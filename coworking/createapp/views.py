from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import CreateAdForm, ImageForm
from .geo_checker import check_address
from .models import OfferImages


@transaction.atomic
def add_ad(request):
    if request.method == 'POST':
        form = CreateAdForm(data=request.POST, files=request.FILES)
        image_form = ImageForm(data=request.POST, files=request.FILES)
        if form.is_valid() and image_form.is_valid():
            try:
                address = check_address(form.cleaned_data['address'])
                room = form.save(commit=False)
                # form.user = request.user
                address.save()
                room.address = address
                room.save()
                for image in image_form.files.getlist('image'):
                    OfferImages.objects.create(room=room, image=ContentFile(image.read(), image.name))

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
