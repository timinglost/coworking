"""mainapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', main, name='main'),
    path('contact/', edit_contacts, name='contact'),

    path('question-category/', question_category, name='question_category'),
    path('question-category/edit/<int:pk>/', category, name='category_edit'),
    path('question-category/add/', add_category, name='category_add'),
    path('question-category/delete/<int:pk>/', delete_category, name='category_delete'),

    path('questions/<int:pk>/', questions, name='questions'),
    path('questions/<int:pk_cat>/edit/<int:pk>/', question_edit, name='questions_edit'),
    path('questions/add/<int:pk_cat>', question_add, name='question_add'),
    path('questions/<int:pk_cat>/delete/<int:pk>/', question_delete, name='question_delete'),

    path('message/', message, name='message'),
    path('message-get/<int:pk>/', get_message, name='message_get'),
    path('message-delete/<int:pk>/', delete_message, name='message_delete'),
]
