from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
# from authapp.models import UserModel
from userapp.models import UserModel


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserModel
        fields = 'username', 'password',


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}))
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}))
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Логин'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}))

    class Meta:
        model = UserModel
        fields = 'first_name', 'email', 'username', 'password1', 'password2'

    def clean_username(self):
        username = self.cleaned_data.get('username')
        new = UserModel.objects.filter(username=username)
        if new.count():
            raise ValidationError('Пользователь с таким логином уже существует.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        new = UserModel.objects.filter(email=email)
        if new.count():
            raise ValidationError('Такой Емейл адрес уже зарегистрирован на сайте.')
        return email
