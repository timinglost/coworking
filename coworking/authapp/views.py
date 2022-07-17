from django.shortcuts import render, HttpResponseRedirect, redirect

from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from authapp.forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.models import AbstractUser


# ================================================================
# =========================== Login ==============================

def login(request):
    title = 'Pages / Login - NiceAdmin Bootstrap Template'

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
# ====================== Logout ================================
def user_logout(request):
    auth.logout(request)

    return redirect('main')


# ================================================================

class UserRegisterView(CreateView):
    model = AbstractUser
    form_class = UserRegisterForm
    template_name = 'authapp/pages-register.html'
    success_url = reverse_lazy('auth:login')
    success_message = 'Пользователь успешно зарегистрирован.'

    def get_context_data(self, **kwargs):
        context = super(UserRegisterView, self).get_context_data(**kwargs)
        context.update({'title': 'Pages / Register - NiceAdmin Bootstrap Template'})
        return context
