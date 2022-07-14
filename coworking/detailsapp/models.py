from django.db import models

from createapp.models import Room
from userapp.models import UserModel


class CurrentRentals(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    offer = models.ForeignKey(Room, on_delete=models.CASCADE)
    seats = models.PositiveIntegerField(verbose_name='Выбранное кол-во мест')
    start_date = models.DateTimeField(verbose_name='Дата и время начала аренды')
    end_date = models.DateTimeField(verbose_name='Дата и время конца аренды')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма к оплате')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления записи')


class CompletedRentals(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    offer = models.ForeignKey(Room, on_delete=models.CASCADE)
    seats = models.PositiveIntegerField(verbose_name='Выбранное кол-во мест')
    start_date = models.DateTimeField(verbose_name='Дата и время начала аренды')
    end_date = models.DateTimeField(verbose_name='Дата и время конца аренды')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма к оплате')
    # evaluation = models.ForeignKey(Rating, on_delete=models.CASCADE, verbose_name='Оценка и отзыв')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления записи')


class Favorites(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    offer = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления записи')

