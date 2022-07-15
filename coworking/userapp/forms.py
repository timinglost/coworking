from django.forms import ModelForm
from userapp.models import UserModel, LandlordApplicationModel


class UserForm(ModelForm):
    class Meta:
        model = UserModel
        fields = ('company', 'job_tittle', 'country', 'about', 'user_phone', 'twitter', 'vk', 'instagram', 'avatar')


class LandlordApplicationForm(ModelForm):
    class Meta:
        model = LandlordApplicationModel
        fields = '__all__'
