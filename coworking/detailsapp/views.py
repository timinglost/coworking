import os

from django.conf import settings
from datetime import datetime

from django.db.models import Avg, Sum
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from createapp.models import Room, Address, RoomCategory, OfferImages, Convenience, ConvenienceRoom, ConvenienceType
from detailsapp.models import CurrentRentals, Favorites, RatingNames, Evaluations, CompletedRentals, Rating


def get_active_offer(pk):
    return get_object_or_404(Room, pk=pk, is_active=True)


def get_offer_reviews(offer):
    rating_dict = {}
    qs = Evaluations.objects.filter(offer=offer)
    try:
        for rating_obj in RatingNames.objects.all():
            rating_dict[rating_obj.name] = int(qs.filter(rating_name=rating_obj).aggregate(rating=Avg("evaluation"))[
                                                   'rating'])
    except:
        pass
    reviews = Rating.objects.filter(offer=offer)
    sum_rating = None
    try:
        sum_rating = f'{reviews.aggregate(summ=Sum("summary_evaluation"))["summ"] / len(reviews):.1f}'
    except:
        pass
    return rating_dict, list(reviews), sum_rating


def get_offer_context(offer):
    try:
        offer_address = get_object_or_404(Address, pk=offer.address.pk)
        category = get_object_or_404(RoomCategory, pk=offer.category.pk)
        offer_images = OfferImages.objects.filter(room=offer)
        conv_types = []
        conveniences = list(Convenience.objects.all())
        room_conveniences_id = [_.convenience_id for _ in ConvenienceRoom.objects.filter(room_id=offer.pk)]
        for conv_type in ConvenienceType.objects.all():
            type_dict = {}
            conv_types.append(type_dict)
            type_dict['name'] = conv_type.name
            type_dict['conveniences'] = list(
                map(
                    lambda it:
                    {'name': it.name,
                     'id': it.pk,
                     'html': read_template(it.file_name)},
                    filter(lambda it: it.convenience_type == conv_type, conveniences)
                )
            )
        context = {
            'title': offer.name,
            'offer': offer,
            'offer_address': offer_address,
            'category': category,
            'seats_number': [_ for _ in range(1, offer.seats_number + 1)],
            'offer_images': offer_images,
            'owner': offer.room_owner,
            'convenience_types': conv_types,
            'conveniences': conveniences,
            'room_conveniences_id': room_conveniences_id,
        }
        return context
    except:
        return None


def read_template(file_name):
    with open(os.path.join(settings.BASE_DIR,
                           'createapp', 'templates', 'createapp', 'includes', 'amenities', file_name), 'r') as file:
        return file.read().rstrip()


def show_details(request, pk):
    try:
        offer = get_active_offer(pk=pk)
        context = get_offer_context(offer=offer)
        rating_dict, reviews, sum_rating = get_offer_reviews(offer=offer)
        context['rating_dict'] = rating_dict
        context['reviews'] = reviews
        context['sum_rating'] = sum_rating
        if 'user/bookings' in request.META.get('HTTP_REFERER') or \
                'user/locations' in request.META.get('HTTP_REFERER') or \
                'admin' in request.META.get('HTTP_REFERER'):
            context['show'] = False
        else:
            context['show'] = True
        return render(request, 'detailsapp/details.html', context=context)
    except:
        return render(request, 'detailsapp/error.html')


def create_rental(request, pk):
    offer = get_object_or_404(Room, pk=pk)
    start_date = datetime.strptime(f"{request.POST['start_date'] + ' ' + request.POST['start_time']}",
                                   "%Y-%m-%d %H:%M")
    end_date = datetime.strptime(f"{request.POST['end_date'] + ' ' + request.POST['end_time']}",
                                 "%Y-%m-%d %H:%M")
    if start_date == end_date:
        working_hours = int((end_date - start_date).seconds / 3600)
    else:
        working_hours = int((end_date - start_date).days * int((end_date - start_date).seconds / 3600) +
                            int((end_date - start_date).seconds / 3600))
    CurrentRentals(
        user=request.user,
        offer=offer,
        seats=int(request.POST['seats']),
        start_date=start_date,
        end_date=end_date,
        amount=int(offer.payment_per_hour * working_hours),
    ).save()
    return HttpResponseRedirect(reverse('user:bookings'))


def send_review(request, pk):
    if request.method == 'POST':
        rental = get_object_or_404(CurrentRentals, pk=pk)
        qs = RatingNames.objects.all()
        rating_sum = int()
        for name_obj in qs:
            evaluation = int(request.POST[f'rating-value{name_obj.id}'])
            rating_sum += evaluation
            Evaluations(
                user=request.user,
                offer=rental.offer,
                rating_name=name_obj,
                evaluation=evaluation,
            ).save()
        Rating(
            user=request.user,
            offer=rental.offer,
            review_text=request.POST['review-text'],
            summary_evaluation=float(rating_sum / len(qs)),
        ).save()
        CompletedRentals(
            user=request.user,
            offer=rental.offer,
            seats=rental.seats,
            start_date=rental.start_date,
            end_date=rental.end_date,
            amount=rental.amount,
        ).save()
        rental.delete()
        return HttpResponseRedirect(reverse('user:bookings'))
    else:
        rating_names = RatingNames.objects.all()
        context = {
            'title': 'title',
            'rating_names': rating_names,
        }
        return render(request, 'detailsapp/offer_feedback.html', context=context)


def add_favorite(request, pk):
    favorite_offer = Favorites(user=request.user, offer=get_object_or_404(Room, pk=pk))
    favorite_offer.save()
    return HttpResponseRedirect(reverse('user:favorites'))
