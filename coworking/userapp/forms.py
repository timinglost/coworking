from django.forms import ModelForm
from userapp.models import UserModel, LandlordApplicationModel


class UserForm(ModelForm):
    class Meta:
        model = UserModel
        fields = '__all__'


class LandlordApplicationForm(ModelForm):
    class Meta:
        model = LandlordApplicationModel
        fields = '__all__'
