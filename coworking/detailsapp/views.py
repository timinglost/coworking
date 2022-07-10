import os

from django.conf import settings
from datetime import datetime

from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from createapp.models import Room, Address, RoomCategory, OfferImages, Convenience, ConvenienceRoom, ConvenienceType
from detailsapp.models import CurrentRentals


def get_offer_context(pk):
    try:
        offer = get_object_or_404(Room, pk=pk, is_active=True)
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
    context = get_offer_context(pk=pk)
    if context:
        return render(request, 'detailsapp/details.html', context=context)
    else:
        return render(request, 'detailsapp/error.html', context=context)


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
    rental = CurrentRentals(
        # user=request.user,
        offer=offer,
        seats=int(request.POST['seats']),
        start_date=start_date,
        end_date=end_date,
        amount=int(offer.payment_per_hour * working_hours),
    )
    rental.save()
    return HttpResponseRedirect(reverse('user:bookings'))


def add_favorite(request, pk):
    # favorite_offer = Favorites(lessee=request.user, location=get_object_or_404(Room, pk=pk))
    # favorite_offer.save()
    return HttpResponseRedirect(reverse('user:favorites'))
