from django.shortcuts import render

from createapp.models import Room
from mainapp.forms import SearchMainForm


def main(request):
    title = 'ЛОКАЦИЯ | Сервис для поиска коворкинга в России'
    form = SearchMainForm()
    context = {
        'title': title,
        'form': form,
        'rooms': Room.objects.all()[:3]
    }
    return render(request, 'mainapp/index.html', context)
