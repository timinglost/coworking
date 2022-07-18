from django.forms import ModelForm, CharField, PasswordInput
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, PasswordChangeForm
from userapp.models import UserModel


# from phonenumber_field.formfields import PhoneNumberField

class UserForm(ModelForm):
    class Meta:
        model = UserModel
        fields = (
            'first_name', 'last_name', 'username',
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
                                  'required': 'Пароль не соответствует стандартам. '
                                              'Используйте цифры и латинские буквы разных регистров.'})
    new_password2 = CharField(required=True, label='Повторите новый пароль',
                              widget=PasswordInput(attrs={'class': 'form-control'}),
                              error_messages={
                                  'required': 'Пароли не совпадают. Попробуйте еще раз'})