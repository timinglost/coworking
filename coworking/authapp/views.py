from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from authapp.forms import LoginUserForm, UserRegisterForm
from django.contrib.auth.models import AbstractUser


# ================================================================
# =========================== Login ==============================

def login(request):
    title = 'Pages / Login - NiceAdmin Bootstrap Template'

    if request.method == "POST":
        form = LoginUserForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            # for control post data
            print('>>>>>>>> ', username, ':', password)
            # =====================
            user = auth.authenticate(request, username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return redirect('main')
        else:
            print('Ошибка данных!!!', form.errors)
            messages.error(request, form.errors)


    else:
        form = LoginUserForm()

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

class UserRegisterView(CreateView):
    model = AbstractUser
    form_class = UserRegisterForm
    template_name = 'authapp/pages-register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super(UserRegisterView, self).get_context_data(**kwargs)
        context.update({'title': 'Pages / Register - NiceAdmin Bootstrap Template'})
        return context

# def register(request):
#     title = 'Pages / Register - NiceAdmin Bootstrap Template'
#
#     if request.method == "POST":
#         form = UserRegisterForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#         else:
#             print('Ошибка данных!!!', form.errors)
#             messages.error(request, form.errors)
#     else:
#         form = UserRegisterForm()
#
#     context = {
#         'title': title,
#         'form': form,
#     }
#     return render(request, 'authapp/pages-register.html', context)
