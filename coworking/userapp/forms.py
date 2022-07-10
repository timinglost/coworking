from django.forms import ModelForm
from userapp.models import UserModel


class UserForm(ModelForm):
    class Meta:
        model = UserModel
        fields = '__all__'
