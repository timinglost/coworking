from django.shortcuts import render


def show_details(request):
    title = 'Some details'

    context = {
        'title': title,
    }
    return render(request, 'detailsapp/details.html', context)
