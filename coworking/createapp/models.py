from django.db import models

from authapp.models import UserModel


class Address(models.Model):
    city = models.CharField(max_length=100, blank=False, verbose_name='Город')
    street = models.CharField(max_length=100, blank=False, verbose_name='Улица')
    building = models.IntegerField(blank=False, verbose_name='Номер дома')
    latitude = models.DecimalField(max_digits=8, decimal_places=6, verbose_name='Широта')  # координато широты
    longitude = models.DecimalField(max_digits=8, decimal_places=6, verbose_name='Долгота')  # координато долготы
    metro_station = models.CharField(max_length=60, blank=False, verbose_name='Улица')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления записи')


class RoomCategory(models.Model):
    CATEGORIES_TYPE = (
        ('op_sp', 'Open space'),
        ('ofc', 'Office'),
        ('pr_ofc', 'Private office'),
        ('con_rm', 'Conference room'),
        ('vi_std', 'Video studio'),
    )

    name = models.CharField(max_length=40, choices=CATEGORIES_TYPE, verbose_name='Название категории')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления записи')

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=256, verbose_name='Наименование помещения')
    square = models.FloatField(max_length=10, blank=False, verbose_name='Площадь помещения')
    description = models.TextField(blank=False, verbose_name='Описание')
    payment_per_hour = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Оплата в час')
    category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE, related_name='room_category',
                                 verbose_name='Категория')  # ONE TO MANY
    start_working_hours = models.TimeField(
        verbose_name='Время работы помещения с ')  # начало работы помещения, например, 7:00
    end_working_hours = models.TimeField(
        verbose_name='Время завершения работы помещения до ')  # закрытие помещения, например, 23:00
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='room_address', verbose_name='Адрес')
    minimum_booking_time = models.IntegerField(default=0, verbose_name='Минимальное время аренды')
    room_owner = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления записи')

    def __str__(self):
        return f'{self.name} | {self.category.name}'


class Image(models.Model):
    image = models.FileField(upload_to='images/', verbose_name='Фото')
    room = models.ForeignKey(Room, related_name='room_image', on_delete=models.CASCADE)
