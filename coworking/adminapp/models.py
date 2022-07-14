from django.db import models
from userapp.models import UserModel


class Claim(models.Model):
    user_id = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )

    text = models.TextField(
        verbose_name='текст заявителя',
        blank=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_active = models.BooleanField(
        verbose_name='активна',
        default=True)

    def __str__(self):
        return f"{self.user_id.first_name} {self.user_id.last_name}"

    class Meta:
        verbose_name = 'Заявка на получение прав арендодателя'
        verbose_name_plural = 'Заявки на получение прав арендодателя'
