# Generated by Django 4.0.5 on 2022-07-06 19:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('createapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrentRentals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seats', models.PositiveIntegerField(verbose_name='Выбранное кол-во мест')),
                ('start_date', models.DateTimeField(verbose_name='Дата и время начала аренды')),
                ('end_date', models.DateTimeField(verbose_name='Дата и время конца аренды')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма к оплате')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время обновления записи')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='createapp.room')),
            ],
        ),
        migrations.CreateModel(
            name='CompletedRentals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seats', models.PositiveIntegerField(verbose_name='Выбранное кол-во мест')),
                ('start_date', models.DateTimeField(verbose_name='Дата и время начала аренды')),
                ('end_date', models.DateTimeField(verbose_name='Дата и время конца аренды')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма к оплате')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время обновления записи')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='createapp.room')),
            ],
        ),
    ]
