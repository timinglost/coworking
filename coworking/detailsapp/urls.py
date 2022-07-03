from django.contrib import admin
from django.urls import path

from detailsapp.views import show_details

urlpatterns = [
    path('<int:pk>/', show_details, name='details')
]
