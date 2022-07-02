from django import forms

from .models import Room, RoomCategory, Image


class CreateAdForm(forms.Form):
    room_name = forms.CharField(label="Название помещения", widget=forms.TextInput(attrs={'class': 'form-control py-2',
                                                                            'placeholder': 'Наименование помещения'}))
    square = forms.FloatField(label="Площадь помещения",
                            widget=forms.TextInput(attrs={'placeholder': 'Площадь помещения'}))
    description = forms.CharField(label="Описание", widget=forms.Textarea(attrs={'class': 'form-control',
                                                                                 'placeholder': 'Описание',
                                                                                 'rows': 6}))

    payment_per_hour = forms.DecimalField(max_digits=10, decimal_places=2, label="Цена за час (руб.)",
                                          widget=forms.TextInput(attrs={'placeholder': 'Цена в час'}))
    category = forms.ModelChoiceField(label="Категория", queryset=RoomCategory.objects.all(),
                                      empty_label="Категория не выбрана")
    # street = forms.CharField(label="Улица", widget=forms.TextInput(attrs={'class': 'form-control py-2', 'placeholder': 'Улица'}))
    # building = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Номер дома'}))
    phone_number = forms.CharField(min_length=10, widget=forms.TextInput(attrs={'placeholder': 'Номер телефона'}))
    address = forms.CharField(label="Название помещения")
    image = forms.ImageField(label="Фото")
    # email = forms.CharField(widget=forms.EmailInput(attrs={
    #     'class': 'form-control py-4', 'placeholder': 'Input user\' email'}))

    class Meta:
        model = Room

    fields = ('room_name', 'square', 'description', 'payment_per_hour', 'category', 'phone_number', 'address', 'image')


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = Image
        fields = ('image',)
        # widgets = {
        #     'file': ClearableFileInput(attrs={'multiple': True}),
        # }
        # widget is important to upload multiple files
