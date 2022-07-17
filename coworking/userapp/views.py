from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.views import PasswordChangeView
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


@login_required
def user_profile(request):
    title = 'ЛОКАЦИЯ | Профиль пользователя'

    if request.method == 'POST':
        passwd_form = PasswordChangeCustomForm(request.user, request.POST)

        if passwd_form.is_valid():
            user = passwd_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Your password was successfully updated!'))
            print(messages.success)
        else:
            messages.error(request, _('Entered password is incorrect.\n '
                                      'The new password must consist of 8 elements including Latin letters in upper and lower case.'))

    else:
        passwd_form = PasswordChangeCustomForm(request.user, request.GET)
    context = {
        'title': title,
        'passwd_form': passwd_form,
    }
    return render(request, 'userapp/user-profile.html', context)


# =============================================================================


@login_required
def user_bookings(request):
    title = 'ЛОКАЦИЯ | Мои бронирования'
    current_rentals_dict = {}
    for rental in get_user_current_rentals(user=request.user):
        rental_images = OfferImages.objects.filter(room=rental.offer)
        current_rentals_dict[rental] = rental_images

    completed_rentals_dict = {}
    for rental in get_user_completed_rentals(user=request.user):
        rental_images = OfferImages.objects.filter(room=rental.offer)
        completed_rentals_dict[rental] = rental_images

    context = {
        'title': title,
        'current_rentals_dict': current_rentals_dict,
        'completed_rentals_dict': completed_rentals_dict,
    }
    return render(request, 'userapp/user-bookings.html', context)


@login_required
def user_locations(request):
    title = 'ЛОКАЦИЯ | Мои локации'
    offers_dict = {}
    for offer in get_user_offers(user=request.user):
        offer_images = OfferImages.objects.filter(room=offer)
        offers_dict[offer] = offer_images
    context = {
        'title': title,
        'offers_dict': offers_dict
    }
    return render(request, 'userapp/user-locations.html', context)


@login_required
def user_favorites(request):
    title = 'ЛОКАЦИЯ | Избранное'
    favorites_dict = {}
    for favorite in get_user_favorites_offers(user=request.user):
        favorite_images = OfferImages.objects.filter(room=favorite.offer)
        favorites_dict[favorite] = favorite_images
    context = {
        'title': title,
        'favorites_dict': favorites_dict,
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
