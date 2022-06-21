from django.shortcuts import render


def main(request):
    title = 'ЛОКАЦИЯ | Сервис для поиска коворкинга в России'


    context = {
        'title': title,
    }
    return render(request, 'mainapp/index.html', context)


