from django import forms
from django.core.exceptions import ValidationError

from feedbackapp.models import Contact, QuestionCategory, Question
import re


class ContactEditForm(forms.ModelForm):
    first_address = forms.CharField(widget=forms.TextInput(
        attrs={'type': "text", 'value': "{{ contacts.first_address }}", 'name': "first_address", 'class': "form-control", 'id': "inputFirstAddress"}))
    second_address = forms.CharField(widget=forms.TextInput(
        attrs={'type': "text", 'value': "{{ contacts.second_address }}", 'name': "second_address", 'class': "form-control", 'id': "inputSecondAddress"}))
    first_phone = forms.CharField(widget=forms.TextInput(
        attrs={'type': "text", 'value': "{{ contacts.first_phone }}", 'name': "first_phone", 'class': "form-control", 'id': "input_first_phone"}))
    second_phone = forms.CharField(widget=forms.TextInput(
        attrs={'type': "text", 'value': "{{ contacts.second_phone }}", 'name': "second_phone", 'class': "form-control", 'id': "input_second_phone"}))
    first_mail = forms.CharField(widget=forms.EmailInput(
        attrs={'type': "email", 'value': "{{ contacts.first_mail }}", 'name': "first_mail", 'class': "form-control", 'id': "first_mail"}))
    second_mail = forms.CharField(widget=forms.EmailInput(
        attrs={'type': "email", 'value': "{{ contacts.second_mail }}", 'name': "second_mail", 'class': "form-control", 'id': "second_mail"}))
    working_days = forms.CharField(widget=forms.TextInput(
        attrs={'type': "text", 'value': "{{ contacts.working_days }}", 'name': "working_days", 'class': "form-control", 'id': "working_days"}))
    Opening_hours = forms.CharField(widget=forms.TextInput(
        attrs={'type': "text", 'value': "{{ contacts.Opening_hours }}", 'name': "Opening_hours", 'class': "form-control", 'id': "Opening_hours"}))

    class Meta:
        model = Contact
        fields = '__all__'

    def clean_first_mail(self):
        first_mail = self.cleaned_data.get('first_mail')
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if re.fullmatch(regex, first_mail):
            return first_mail
        else:
            raise ValidationError('Инвалидный email.')

    def clean_second_mail(self):
        second_mail = self.cleaned_data.get('second_mail')
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if re.fullmatch(regex, second_mail):
            return second_mail
        else:
            raise ValidationError('Инвалидный email.')

    def clean_first_phone(self):
        first_phone = self.cleaned_data.get('first_phone')
        if len(first_phone) >= 20:
            raise ValidationError('Слишком длинный номер!')
        else:
            return first_phone

    def clean_second_phone(self):
        second_phone = self.cleaned_data.get('second_phone')
        if len(second_phone) >= 20:
            raise ValidationError('Слишком длинный номер!')
        else:
            return second_phone


class QuestionCategoryEditForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'type': "text", 'name': "name",
               'class': "form-control", 'id': "inputText"}))

    class Meta:
        model = QuestionCategory
        fields = 'name',

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) >= 128:
            raise ValidationError('Слишком длинное название!')
        else:
            return name


class QuestionEditForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'type': "text", 'name': "name",
               'class': "form-control", 'id': "inputName"}))
    slug = forms.CharField(widget=forms.TextInput(
        attrs={'type': "text", 'name': "slug",
               'class': "form-control", 'id': "inputSlug"}))
    text = forms.CharField(widget=forms.Textarea(
        attrs={'class': "form-control", 'id': "inputText", 'name': "text", 'rows': "10"}))

    class Meta:
        model = Question
        fields = ['name', 'slug', 'text']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) >= 128:
            raise ValidationError('Слишком длинное имя!')
        else:
            return name
