# Generated by Django 4.0.5 on 2022-07-15 16:24

from django.conf import settings
from django.db import migrations, models, transaction
import django.db.models.deletion


def fill_names(apps, schema_editor):
    with transaction.atomic():
        RatingNames = apps.get_model('detailsapp', 'RatingNames')
        for name in ['Качество помещения', 'Рабочая обстановка', 'Качество удобств', 'Соответствие цена-качество',
                     'Соответствие фото']:
            obj = RatingNames()
            obj.name = name
            obj.save()


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('createapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RatingNames',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Наименование критерия')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время обновления записи')),
            ],
        ),
        migrations.CreateModel(
            name='OffersRatings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary_rating', models.FloatField(verbose_name='Суммарная оценка')),
                ('reviews_number', models.PositiveIntegerField(verbose_name='Количество отзывов')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время обновления записи')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='createapp.room')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_text', models.TextField(verbose_name='Отзыв')),
                ('summary_evaluation', models.FloatField(verbose_name='Суммарная оценка')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время обновления записи')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='createapp.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время обновления записи')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='createapp.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Evaluations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evaluation', models.PositiveIntegerField(verbose_name='Оценка')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время обновления записи')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='createapp.room')),
                ('rating_name',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='detailsapp.ratingnames',
                                   verbose_name='Название')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
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
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CompletedRentals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seats', models.PositiveIntegerField(verbose_name='Выбранное кол-во мест')),
                ('start_date', models.DateTimeField(verbose_name='Дата и время начала аренды')),
                ('end_date', models.DateTimeField(verbose_name='Дата и время конца аренды')),
                ('amount', models.PositiveIntegerField(verbose_name='Сумма к оплате')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время обновления записи')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='createapp.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RunPython(fill_names),
    ]