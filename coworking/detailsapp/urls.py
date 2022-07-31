from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from detailsapp.views import show_details, create_rental, add_favorite, send_review, get_available_seats, del_favorite

urlpatterns = [
    path('<int:pk>/', show_details, name='details'),
    path('<int:pk>/add_fav/', add_favorite, name='add_favorite'),
    path('<int:pk>/del_fav/', del_favorite, name='del_favorite'),
    path('new_rent/<int:pk>/', create_rental, name='create_rental'),
    path('review/<int:pk>/', send_review, name='send_review'),
    path('<int:pk>/<str:start_date>/<str:end_date>/<int:seats>/',
         get_available_seats, name='get_seats')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
