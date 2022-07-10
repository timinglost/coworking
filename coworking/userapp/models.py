from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone
from django.db import models


# Create your models here.

class UserModel(AbstractUser):
    avatar = models.ImageField(upload_to='authapp/media/users_avatar', blank=True, verbose_name='Аватар пользователя')
    company = models.CharField(max_length=50, blank=True, verbose_name='Компания')
    job_tittle = models.CharField(max_length=50, blank=True, verbose_name='Профессия')
    country = models.CharField(max_length=50, blank=True, verbose_name='Страна')
    about = models.TextField(max_length=200, blank=True)
    user_phone = models.CharField(max_length=15,
                                  validators=[RegexValidator(r'^\d{1,15}$')], verbose_name='Телефон', blank=True)

    # address = AddressField(blank=True, on_delete=models.CASCADE)
    # user_phone = PhoneNumberField(blank=True, region='IT')

    is_moderator = models.BooleanField(default=False,
                                       help_text=_(
                                           'Designates whether the user can control the request '
                                           'to create a rental card.'))
    is_landlord = models.BooleanField(default=False,
                                      help_text=_(
                                          'Designates whether the user can '
                                          'to create a rental card.'))
    twitter = models.CharField(verbose_name='Профиль в триттере', max_length=64, blank=True)
    vk = models.CharField(verbose_name='Профиль в контакте', max_length=64, blank=True)
    instagram = models.CharField(verbose_name='Профиль в инстаграме', max_length=64, blank=True)

    created_at = models.DateTimeField(editable=False, verbose_name='Пользователь зарегистрирован')
    updated_at = models.DateTimeField(verbose_name='Пользователь обновлен')

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def save(self, *args, **kwargs):
        """On save, update timestamps """
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(UserModel, self).save(*args, **kwargs)
