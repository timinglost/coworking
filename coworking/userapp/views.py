from django.shortcuts import render


def users(request):
    title = 'ЛОКАЦИЯ | Личный кабинет'


    context = {
        'title': title,
    }
    return render(request, 'userapp/users.html', context)


def users_profile(request):
    title = 'ЛОКАЦИЯ | Профиль ползователя'


    context = {
        'title': title,
    }
    return render(request, 'userapp/users-profile.html', context)


def users_bookings(request):
    title = 'ЛОКАЦИЯ | Мои бронирования'


    context = {
        'title': title,
    }
    return render(request, 'userapp/users-bookings.html', context)


def users_favorites(request):
    title = 'ЛОКАЦИЯ | Мои бронирования'


    context = {
        'title': title,
    }
    return render(request, 'userapp/users-favorites.html', context)
