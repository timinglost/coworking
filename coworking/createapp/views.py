from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import CreateAdForm
from .geo_checker import check_address


def add_ad(request):
    if request.method == 'POST':
        form = CreateAdForm(data=request.POST)
        if form.is_valid():
            try:
                address = check_address(form.cleaned_data['address'])
                room = form.save(commit=False)
                address.save()
                room.address = address
                room.save()
            except ValidationError as e:
                form.add_error('address', e)
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = CreateAdForm()

    context = {
        'title': 'Добавить новое объявление',
        'form': form,
    }
    return render(request, 'createapp/advertisement.html', context)
