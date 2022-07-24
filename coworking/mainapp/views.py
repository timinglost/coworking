from django.shortcuts import render

from createapp.models import Room, OfferImages
from mainapp.forms import SearchMainForm


def main(request):
    title = 'ЛОКАЦИЯ | Сервис для поиска коворкинга в России'
    form = SearchMainForm()
    rooms = list(Room.objects.all()[:3])
    offer_images = OfferImages.objects.filter(room__in=rooms)
    context = {
        'title': title,
        'form': form,
        'offer_images': offer_images
    }
    return render(request, 'mainapp/index.html', context)
