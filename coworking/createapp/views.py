from django.shortcuts import render

from .forms import CreateAdForm


def add_ad(request):
    form = CreateAdForm()
    context = {
        'title': 'Добавить новое объявление',
        'form': form,
    }
    return render(request, 'createapp/advertisement.html', context)


