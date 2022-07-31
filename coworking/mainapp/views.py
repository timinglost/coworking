import numpy
from django.db.models import Avg
from django.shortcuts import render, redirect

from createapp.models import Room, OfferImages
from detailsapp.models import OffersRatings, Evaluations, RatingNames
from feedbackapp.models import Contact, QuestionCategory, Question
from mainapp.forms import SearchMainForm
from userapp.models import UserModel


def get_top_landlords():
    all_landlords = {}
    for room in [_ for _ in Room.objects.filter(room_owner__is_landlord=True, is_active=True, is_published=True) if
                 _ in [_.offer for _ in OffersRatings.objects.all()]]:
        all_landlords[room.room_owner] = f"{numpy.average([OffersRatings.objects.get(offer=room).summary_rating]):.1f}"
    return [k for k, v in sorted(all_landlords.items(), key=lambda item: item[1])[:3]]


def avg_rating_per_criteria(landlord, criteria_name):
    room_ratings = [
        Evaluations.objects.filter(offer=room).filter(rating_name=criteria_name).aggregate(
            rating=Avg("evaluation"))['rating']
        for room in [_ for _ in Room.objects.filter(room_owner=landlord, is_active=True, is_published=True) if
                 _ in [_.offer for _ in OffersRatings.objects.all()]]
    ]
    room_ratings = list(map(lambda it: int(it), room_ratings))
    return int(numpy.average(room_ratings) * 10) if len(room_ratings) > 0 else 0


def main(request):
    title = 'ЛОКАЦИЯ | Сервис для поиска коворкинга в России'

    has_query = len(request.GET) > 0

    if has_query:
        form = SearchMainForm(data=request.GET)
    else:
        form = SearchMainForm()
    offer_ratings = list(OffersRatings.objects.order_by('-summary_rating')[:3])
    rooms = list(map(lambda x: x.offer if x.offer.is_active and x.offer.is_published else None, offer_ratings))
    offer_images = OfferImages.objects.filter(room__in=rooms)

    room_data = {}

    for room in rooms:
        if room:
            room_data[room] = {
                'rating': OffersRatings.objects.get(offer=room).summary_rating
            }
    rating_names = RatingNames.objects.all()
    top_landlords = {
        landlord: {
            name: avg_rating_per_criteria(landlord, name) for name in rating_names
        } for landlord in get_top_landlords()
    }
    for image in offer_images:
        room_data[image.room]['image'] = image.image
    context = {
        'title': title,
        'form': form,
        'room_data': room_data,
        'contact_data': Contact.objects.first(),
        'for_users': Question.objects.filter(category=QuestionCategory.objects.filter(name="Пользователям").first()),
        'for_landlords': Question.objects.filter(
            category=QuestionCategory.objects.filter(name="Арендодателям").first()),
        'top_landlords': top_landlords
    }
    if has_query and form.is_valid():
        return redirect('offers/search/?' + request.GET.urlencode())
    return render(request, 'mainapp/index.html', context)
