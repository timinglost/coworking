from django import forms
from django.core.validators import RegexValidator
from django.forms import ModelForm

from .models import Room, RoomCategory


class CreateAdForm(ModelForm):
    name = forms.CharField(label="Наименование помещения",
                                initial='Room Name',
                                widget=forms.TextInput(attrs={'class': 'form-control py-2',
                                                              'placeholder': 'Наименование помещения'}))
    square = forms.FloatField(label="Площадь помещения",
                              initial=70,
                              widget=forms.TextInput(attrs={'placeholder': 'Площадь помещения'}))
    description = forms.CharField(label="Описание",
                                  initial="Description",
                                  widget=forms.Textarea(attrs={'class': 'form-control',
                                                               'placeholder': 'Описание',
                                                               'rows': 6}))

    payment_per_hour = forms.DecimalField(max_digits=10, initial=1000, decimal_places=2, label="Цена за час (руб.)",
                                          widget=forms.TextInput(attrs={'placeholder': 'Цена в час'}))
    category = forms.ModelChoiceField(label="Категория", queryset=RoomCategory.objects.all(),
                                      empty_label="Категория не выбрана")
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phone_number = forms.CharField(min_length=10, initial=89995555555,
                                   validators=[phoneNumberRegex],
                                   widget=forms.TextInput(attrs={'placeholder': 'Номер телефона'}))
    address = forms.CharField(label="Название помещения",
                              min_length=7,
                              widget=forms.TextInput(
                                  attrs={'id': 'address', 'placeholder': 'Введите адрес', 'style': 'width: 100%'}))

    # image = forms.ImageField(label="Фото")

    # email = forms.CharField(widget=forms.EmailInput(attrs={
    #     'class': 'form-control py-4', 'placeholder': 'Input user\' email'}))

    class Meta:
        model = Room
        fields = ['name', 'square', 'description', 'payment_per_hour', 'category', 'phone_number']

# class ImageForm(forms.ModelForm):
#     image = forms.ImageField(label='Image')

# class Meta:
#     model = Image
#     fields = ('image',)
# widgets = {
#     'file': ClearableFileInput(attrs={'multiple': True}),
# }
# widget is important to upload multiple files
