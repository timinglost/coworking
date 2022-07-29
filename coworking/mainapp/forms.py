from django import forms
from django.forms import Form


class DateInput(forms.DateInput):
    input_type = 'date'


class SearchMainForm(Form):
    city = forms.CharField(label="Адрес",
                           required=True,
                           widget=forms.TextInput(attrs={'id': 'suggest', 'class': 'form-control',
                                                         'placeholder': 'Город'}))
    date = forms.DateField(label="Дата",
                           required=False,
                           widget=DateInput(attrs={'id': 'dateIn', 'class': 'form-control',
                                                   'placeholder': 'Дата'}))
