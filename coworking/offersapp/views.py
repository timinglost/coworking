from django.shortcuts import render


def offers(request):
    title = 'ЛОКАЦИЯ | Поиск помещений'

    context = {
        'title': title,
    }
    return render(request, 'offersapp/offers.html', context)
