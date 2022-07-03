from django.shortcuts import render, get_object_or_404

from createapp.models import Room, Address, RoomCategory


def show_details(request, pk):
    offer = get_object_or_404(Room, pk=pk)
    offer_address = get_object_or_404(Address, pk=offer.address.pk)
    category = get_object_or_404(RoomCategory, pk=offer.category.pk)
    # offer_photos = get_object_or_404(Images, pk=offer.image.pk)

    context = {
        'title': offer.name,
        'offer': offer,
        'offer_address': offer_address,
        'category': category,
        # "seats_number": [_ for _ in range(1, offer.seats_number + 1)],
        # 'offer_photos': offer_photos,
    }
    return render(request, 'detailsapp/details.html', context=context)
