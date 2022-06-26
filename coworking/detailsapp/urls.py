from django.contrib import admin
from django.urls import path

from coworking.detailsapp.views import show_details

urlpatterns = [
    path('', show_details, name='details')
]
