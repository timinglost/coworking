from django.shortcuts import render

from mainapp.forms import SearchMainForm


def main(request):
    title = 'ЛОКАЦИЯ | Сервис для поиска коворкинга в России'
    form = SearchMainForm()
    rooms = []
    context = {
        'title': title,
        'form': form,
        'rooms': rooms
    }
    return render(request, 'mainapp/index.html', context)


