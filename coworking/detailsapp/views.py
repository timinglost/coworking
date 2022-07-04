from django.shortcuts import render, get_object_or_404

from createapp.models import Room, Address, RoomCategory  # OfferImages


def show_details(request, pk):
    offer = get_object_or_404(Room, pk=pk)
    offer_address = get_object_or_404(Address, pk=offer.address.pk)
    category = get_object_or_404(RoomCategory, pk=offer.category.pk)
    # offer_images = offer.prefetch_related('room_images')

    context = {
        'title': offer.name,
        'offer': offer,
        'offer_address': offer_address,
        'category': category,
        # "seats_number": [_ for _ in range(1, offer.seats_number + 1)],
        # 'offer_images': offer_images,
    }
    return render(request, 'detailsapp/details.html', context=context)
