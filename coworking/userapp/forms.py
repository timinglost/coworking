from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
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
