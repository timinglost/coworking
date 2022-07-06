from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from detailsapp.views import show_details, create_rental, add_favorite


urlpatterns = [
    path('<int:pk>/', show_details, name='details'),
    path('add_fav/<int:pk>/', add_favorite, name='add_favorite'),
    path('new_rent/<int:pk>/', create_rental, name='create_rental'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
