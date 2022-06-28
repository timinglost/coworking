from django.db import models


class RoomCategory(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='Название категории')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Время обновления записи')  # обновляет значение поля до текущего времени и даты каждый раз

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=256, verbose_name='Наименование помещения')
    area = models.FloatField(max_length=10, blank=False, verbose_name='Площадь помещения')
    description = models.TextField(blank=False, verbose_name='Описание')
    payment_per_hour = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Оплата в час')
    category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE, verbose_name='Категория')  # ONE TO MANY
    # image = models.ImageField(upload_to='images/', verbose_name='Фото')
    start_working_hours = models.TimeField(
        verbose_name='Время работы помещения с ')  # начало работы помещения, например, 7:00
    end_working_hours = models.TimeField(
        verbose_name='Время завершения работы помещения до ')  # закрытие помещения, например, 23:00
    # address_id =
    minimum_booking_time = models.IntegerField(default=0, verbose_name='Минимальное время аренды')
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления записи')

    def __str__(self):
        return f'{self.name} | {self.category.name}'


class Image(models.Model):
    image = models.FileField(upload_to='images/', verbose_name='Фото')
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
