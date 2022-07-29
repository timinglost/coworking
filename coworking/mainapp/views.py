from django.shortcuts import render, redirect

from createapp.models import Room, OfferImages
from mainapp.forms import SearchMainForm


def main(request):
    title = 'ЛОКАЦИЯ | Сервис для поиска коворкинга в России'

    has_query = len(request.GET) > 0

    if has_query:
        form = SearchMainForm(data=request.GET)
    else:
        form = SearchMainForm()
    rooms = list(Room.objects.all()[:3])
    offer_images = OfferImages.objects.filter(room__in=rooms)
    context = {
        'title': title,
        'form': form,
        'offer_images': offer_images
    }
    if has_query and form.is_valid():
        return redirect('offers/search/?' + request.GET.urlencode())
    return render(request, 'mainapp/index.html', context)
