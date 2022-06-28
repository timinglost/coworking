from django.shortcuts import render


def main(request):
    title = 'ЛОКАЦИЯ | Поиск помещений'

    context = {
        'title': title,
    }
    return render(request, 'offersapp/index.html', context)
