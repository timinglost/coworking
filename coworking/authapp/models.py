from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class UserModel(AbstractUser):
    avatar = models.ImageField(upload_to='authapp/media/users_avatar', blank=True)
