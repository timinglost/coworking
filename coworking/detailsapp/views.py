from datetime import datetime

from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from createapp.models import Room, Address, RoomCategory  # OfferImages
from detailsapp.models import CurrentRentals


def get_offer_context(pk):
    offer = get_object_or_404(Room, pk=pk)
    offer_address = get_object_or_404(Address, pk=offer.address.pk)
    category = get_object_or_404(RoomCategory, pk=offer.category.pk)
    # offer_images = offer.prefetch_related('room_images')
    # запросы в таблицу категорий удобств и выборка категория + удобства этой категории

    context = {
        'title': offer.name,
        'offer': offer,
        'offer_address': offer_address,
        'category': category,
        # 'seats_number': [_ for _ in range(1, offer.seats_number + 1)],
        'seats_number': [_ for _ in range(1, 16)],
        # 'offer_images': offer_images,
        # 'convenience_types': convenience_types,
        # 'conveniences': conveniences,
    }
    return context


def show_details(request, pk):
    context = get_offer_context(pk=pk)
    return render(request, 'detailsapp/details.html', context=context)


def create_rental(request, pk):
    offer = get_object_or_404(Room, pk=pk)
    start_date = datetime.strptime(f"{request.POST['start_date'] + ' ' + request.POST['start_time']}",
                                   "%Y-%m-%d %H:%M")
    end_date = datetime.strptime(f"{request.POST['end_date'] + ' ' + request.POST['end_time']}",
                                 "%Y-%m-%d %H:%M")
    working_hours = None
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
    # favorite_offer = Favorites(user=request.user, offer=get_object_or_404(Room, pk=pk))
    # favorite_offer.save()
    return HttpResponseRedirect(reverse('user:favorites'))
