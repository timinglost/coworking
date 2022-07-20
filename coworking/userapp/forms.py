from django.forms import ModelForm, CharField, PasswordInput, ClearableFileInput
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, PasswordChangeForm
from userapp.models import UserModel, LandlordApplicationModel
from adminapp.models import Claim
from django.core.exceptions import ValidationError


# from phonenumber_field.formfields import PhoneNumberField

class UserForm(ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'type': "text",  'name': "first_name", 'class': "form-control", 'id': "firstName"}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'type': "text",  'name': "last_name", 'class': "form-control", 'id': "lastName"}))
    about = forms.CharField(widget=forms.Textarea(
        attrs={'class': "form-control", 'name': "about", 'id': "about", 'style': "height: 100px"}))
    company = forms.CharField(widget=forms.TextInput(
        attrs={'type': "text",  'name': "company", 'class': "form-control", 'id': "company"}))
    job_tittle = forms.CharField(widget=forms.TextInput(
        attrs={'type': "text",  'name': "job_tittle", 'class': "form-control", 'id': "job_tittle"}))
    country = forms.CharField(widget=forms.TextInput(
        attrs={'type': "text",  'name': "country", 'class': "form-control", 'id': "country"}))
    user_phone = forms.CharField(widget=forms.TextInput(
        attrs={'type': "text",  'name': "user_phone", 'class': "form-control", 'id': "user_phone"}))
    email = forms.CharField(widget=forms.TextInput(
        attrs={'type': "text",  'name': "email", 'class': "form-control", 'id': "email"}))
    twitter = forms.CharField(widget=forms.TextInput(
        attrs={'type': "text",  'name': "twitter", 'class': "form-control", 'id': "twitter"}))
    vk = forms.CharField(widget=forms.TextInput(
        attrs={'type': "text",  'name': "vk", 'class': "form-control", 'id': "vk"}))
    instagram = forms.CharField(widget=forms.TextInput(
        attrs={'type': "text",  'name': "instagram", 'class': "form-control", 'id': "instagram"}))
    avatar = forms.ImageField(required=False, widget=ClearableFileInput(
        attrs={'class': 'file-input', 'name': "avatar", 'id': 'formFile'}))

    class Meta:
        model = UserModel
        fields = (
            'first_name', 'last_name',
            'country', 'user_phone', 'email',
            'avatar', 'about', 'company', 'job_tittle',
            'twitter', 'vk', 'instagram')


    # def __int__(self, *args, **kwargs):
    #     super(UserForm, self).__int__(*args, **kwargs)
    #
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'


class PasswordChangeCustomForm(PasswordChangeForm):
    error_css_class = 'has-error'

    error_messages = {'password_incorrect':
                          "Password incorrect. Please try again."}

    old_password = CharField(required=True, label='Старый пароль', widget=PasswordInput(
        attrs={'class': 'form-control'}),
                             error_messages={'required': 'Неверно введен пароль.'})

    new_password1 = CharField(required=True, label='Новый пароль',
                              widget=PasswordInput(attrs={'class': 'form-control'}),
                              error_messages={
                                  'required': 'Пароль не соответствует стандартам. Используйте цифры и латинские буквы разных регистров.'})
    new_password2 = CharField(required=True, label='Повторите новый пароль',
                              widget=PasswordInput(attrs={'class': 'form-control'}),
                              error_messages={
                                  'required': 'Пароли не совпадают. Попробуйте еще раз'})

    def clean_new_password2(self):

        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    'Пароли не совпадают! '
                    'Пожалуйста введите новый пароль и повторите его для подтверждения.'
                )
        return password2


class LandlordApplicationForm(ModelForm):
    text = forms.CharField(widget=forms.Textarea(
        attrs={'class': "form-control", 'id': "inputText", 'name': "text", 'rows': "10"}))

    class Meta:
        model = Claim
        fields = ['text']
