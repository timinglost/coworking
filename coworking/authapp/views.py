from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import auth, messages
from django.urls import reverse
from authapp.forms import LoginUserForm, UserRegisterForm


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

def register(request):
    title = 'Pages / Register - NiceAdmin Bootstrap Template'

    if request.method == "POST":
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print('Ошибка данных!!!', form.errors)
            messages.error(request, form.errors)
    else:
        form = UserRegisterForm(data=request.GET)

    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'authapp/pages-register.html', context)
