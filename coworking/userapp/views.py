from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib import auth, messages
from django.shortcuts import redirect

from createapp.models import Room, OfferImages
from detailsapp.models import CurrentRentals, CompletedRentals, Favorites
from userapp.models import UserModel
from userapp.forms import UserForm
from django.urls import reverse_lazy

from userapp.forms import PasswordChangeCustomForm


@login_required
def user(request):
    title = 'ЛОКАЦИЯ | Личный кабинет'

    context = {
        'title': title,
    }
    return render(request, 'userapp/user.html', context)


def get_user_offers(user):
    return Room.objects.filter(room_owner=user)


def get_user_current_rentals(user):
    return CurrentRentals.objects.filter(user=user)


def get_user_completed_rentals(user):
    return CompletedRentals.objects.filter(user=user)


def get_user_favorites_offers(user):
    return Favorites.objects.filter(user=user)


def get_room_images(rooms):
    offers_dict = {}
    for room in rooms:
        room_images = OfferImages.objects.filter(room=room)
        # room_images = [_ for _ in room_images]
        offers_dict[room] = room_images
    return offers_dict


@login_required
def user_profile(request):
    title = 'ЛОКАЦИЯ | Профиль пользователя'
    if request.method == 'POST':
        form = PasswordChangeCustomForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Your password was successfully updated!'))
            return redirect('main')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = PasswordChangeCustomForm(request.user)

    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'userapp/user-profile.html', context)


@login_required
def user_bookings(request):
    title = 'ЛОКАЦИЯ | Мои бронирования'

    context = {
        'title': title,
        'offers_dict': get_room_images(rooms=[_.offer for _ in get_user_current_rentals(user=request.user)]),
    }
    return render(request, 'userapp/user-bookings.html', context)


@login_required
def user_locations(request):
    title = 'ЛОКАЦИЯ | Мои локации'

    context = {
        'title': title,
        'offers_dict': get_room_images(rooms=get_user_offers(user=request.user)),
    }
    return render(request, 'userapp/user-locations.html', context)


@login_required
def user_favorites(request):
    title = 'ЛОКАЦИЯ | Избранное'

    context = {
        'title': title,
        'offers_dict': get_room_images(rooms=[_.offer for _ in get_user_favorites_offers(user=request.user)]),
    }
    return render(request, 'userapp/user-favorites.html', context)


class UserCreateView(CreateView):
    template_name = 'userapp/user-edit.html'
    form_class = UserForm
    success_url = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context.update({'title': 'Редактирование профиля'})
        return context
