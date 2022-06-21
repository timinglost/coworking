from django.shortcuts import render


def login(request):
    title = 'Pages / Login - NiceAdmin Bootstrap Template'


    context = {
        'title': title,
    }
    return render(request, 'authapp/pages-login.html', context)


def logout(request):
    pass


def register(request):
    title = 'Pages / Register - NiceAdmin Bootstrap Template'


    context = {
        'title': title,
    }
    return render(request, 'authapp/pages-register.html', context)
