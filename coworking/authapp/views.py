from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.utils.translation import gettext as _

from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from authapp.forms import UserRegisterForm, UserLoginForm, LandlordRegisterForm
from django.contrib.auth.models import AbstractUser
from userapp.models import UserModel

from django.conf import settings

# ================================================================
# =========================== Login ==============================
from userapp.models import UserModel


def login(request):
    title = 'Авторизация'

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

def choose_type(request):
    return render(request, 'authapp/choose_type.html')


class UserRegisterView(CreateView):
    model = UserModel
    form_class = UserRegisterForm
    template_name = 'authapp/user-register.html'
    success_url = reverse_lazy('auth:login')
    success_message = 'Пользователь успешно зарегистрирован.'

    # функция send_mail, спецклас

    def form_valid(self, form):

        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # to get the domain of the current site
            if send_verify_mail(user):
                messages.success(self.request, _('Сообщение подтверждения регистрации отправленно на почту.'))
                print('Сообщение подтверждения регистрации отправленно на почту.')
                return redirect('auth:login')
            else:
                messages.error(self.request, _('Ошибка отправки сообщения!'))
                print('Ошибка отправки сообщения!')
                return redirect('auth:register')

        return super(UserRegisterView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UserRegisterView, self).get_context_data(**kwargs)
        context.update({'title': 'Регистрация пользователя'})
        return context


class LandlordRegisterView(CreateView):
    model = UserModel
    form_class = LandlordRegisterForm
    template_name = 'authapp/landlord-register.html'
    success_url = reverse_lazy('auth:login')
    success_message = 'Арендодатель успешно зарегистрирован.'

    def get_context_data(self, **kwargs):
        context = super(LandlordRegisterView, self).get_context_data(**kwargs)
        context.update({'title': 'Регистрация арендодателя'})
        return context


# ===================================================
def verify(request, email, activation_key):
    # user = UserModel.objects.filter(email).first()
    user = UserModel.objects.filter(email=email).first()
    if user:
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            # auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return render(request, 'authapp/page-confirm-register.html')

    return redirect('main')


from django.template.loader import render_to_string


def send_verify_mail(user):
    subject = 'Verify your account'
    link = reverse('authapp:verify', args=[user.email, user.activation_key])
    template = render_to_string('authapp/email_template.html',
                                {'name': user.username, 'link': f"{settings.DOMAIN}{link}"})

    return send_mail(
        subject,  # subject
        template,  # message
        settings.EMAIL_HOST_USER,  # from_email
        [user.email],  # recipient_list - список получателей
        fail_silently=False, auth_password='zbdjzgrddsiaufqs')

    # ===================================================
