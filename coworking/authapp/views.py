from django.shortcuts import render, HttpResponseRedirect, redirect

from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from authapp.forms import UserRegisterForm, UserLoginForm, LandlordRegisterForm
from django.contrib.auth.models import AbstractUser

# ================================================================
# =========================== Login ==============================
from userapp.models import UserModel


def login(request):
    title = 'ЛОКАЦИЯ | Авторизация'

    if request.method == "POST":
        form = UserLoginForm(data=request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            # =====================
            user = auth.authenticate(request, username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return redirect('main')
        else:
            print('Ошибка данных!!!', form.errors)
            messages.error(request, form.errors)

    else:
        if request.user.is_active:
            return redirect('main')

        form = UserLoginForm(data=request.GET)

    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'authapp/pages-login.html', context)


# ================================================================
# ====================== Complete ================================
def user_logout(request):
    auth.logout(request)

    return redirect('main')


# ================================================================

def choose_type(request):
    return render(request, 'authapp/choose_type.html', {'title': 'ЛОКАЦИЯ | Регистрация'})


class UserRegisterView(CreateView):
    model = UserModel
    form_class = UserRegisterForm
    template_name = 'authapp/user-register.html'
    success_url = reverse_lazy('auth:login')
    success_message = 'Пользователь успешно зарегистрирован.'

    def get_context_data(self, **kwargs):
        context = super(UserRegisterView, self).get_context_data(**kwargs)
        context.update({'title': 'ЛОКАЦИЯ | Регистрация пользователя'})
        return context


class LandlordRegisterView(CreateView):
    model = UserModel
    form_class = LandlordRegisterForm
    template_name = 'authapp/landlord-register.html'
    success_url = reverse_lazy('auth:login')
    success_message = 'Арендодатель успешно зарегистрирован.'

    def get_context_data(self, **kwargs):
        context = super(LandlordRegisterView, self).get_context_data(**kwargs)
        context.update({'title': 'ЛОКАЦИЯ | Регистрация арендодателя'})
        return context
