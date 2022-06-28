from django import forms

from .models import Room, RoomCategory, Image


class CreateAdForm(forms.Form):
    room_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-2',
                                                              'placeholder': 'Наименование помещения'}))
    area = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Площадь помещения'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание',
                                                               'rows': 6}))
    # email = forms.CharField(widget=forms.EmailInput(attrs={
    #     'class': 'form-control py-4', 'placeholder': 'Input user\' email'}))
    payment_per_hour = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={
    'placeholder': 'Цена в час'}))
    category = forms.ModelChoiceField(queryset=RoomCategory.objects.all())
    # address =
    # city =
    # street =
    # building =
    image = forms.ImageField()
    # phone_number = forms.

    class Meta:

        model = Room
    fields = ('room_name', 'area', 'description', 'payment_per_hour', 'category', 'city', 'street', 'image',
              'phone_number')


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = Image
        fields = ('image',)
        # widgets = {
        #     'file': ClearableFileInput(attrs={'multiple': True}),
        # }
        # widget is important to upload multiple files
