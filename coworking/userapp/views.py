from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from userapp.models import UserModel


@login_required
def user(request):
    title = 'ЛОКАЦИЯ | Личный кабинет'

    context = {
        'title': title,
    }
    return render(request, 'userapp/user.html', context)


@login_required
def user_profile(request):
    title = 'ЛОКАЦИЯ | Профиль пользователя'

    context = {
        'title': title,
    }
    return render(request, 'userapp/user-profile.html', context)


@login_required
def user_bookings(request):
    title = 'ЛОКАЦИЯ | Мои бронирования'

    context = {
        'title': title,
    }
    return render(request, 'userapp/user-bookings.html', context)


@login_required
def user_locations(request):
    title = 'ЛОКАЦИЯ | Мои локации'

    context = {
        'title': title,
    }
    return render(request, 'userapp/user-locations.html', context)


@login_required
def user_favorites(request):
    title = 'ЛОКАЦИЯ | Избранное'

    context = {
        'title': title,
    }
    return render(request, 'userapp/user-favorites.html', context)
