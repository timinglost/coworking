   # Generated by Django 4.0.5 on 2022-07-11 15:33

from django.conf import settings
from django.db import migrations, models, transaction
import django.db.models.deletion


def fill_categories(apps, schema_editor):
    with transaction.atomic():
        RoomCategory = apps.get_model('createapp', 'RoomCategory')
        for cat in ['Open space', 'Office', 'Private office', 'Conference room', 'Video studio']:
            category = RoomCategory()
            category.name = cat
            category.save()


def fill_convenience(apps, schema_editor):
    with transaction.atomic():
        ConvenienceType = apps.get_model('createapp', 'ConvenienceType')
        Convenience = apps.get_model('createapp', 'Convenience')
        for convenience_type in [
            ('Ключевые удобства', [('Wi-Fi', 'wifi.html'), ('Современный ремонт', 'modern_repair.html'),
                                   ('Высокоскоростной интернет', 'high-speed_Internet.html'),
                                   ('Мебель', 'furniture.html'), ('Охрана', 'security.html')]),
            ('Еда и напитки', [('Еда и напитки', 'drinks.html'), ('Закуски/фрукты', 'snacks.html'),
                               ('Кухня', 'kitchen.html'), ('Cafe', 'cafe.html')]),
            ('Оборудование', [('Принтер/сканер', 'scanner.html'), ('Факс', 'fax.html'),
                              ('Флипчарт', 'flipchart.html')]),
            ('Специальные зоны', [('Переговорные комнаты', 'conference_room.html'), ('Телефон', 'phone.html'),
                                  ('Шкафчики', 'locker.html')]),
            ('Услуги', [('Техническая поддержка', 'support.html'), ('Ресепшн', 'reception.html'),
                        ('Клининг', 'cleaning.html')]),
            ('Общение', [('Зоны отдыха', 'relax.html'), ('Мероприятия', 'events.html')]),
            ('Транспорт', [('Парковка', 'parking.html'), ('Велопарковка', 'bike_parking.html')]),
            ('Здоровье', [('Спортзал', 'gym.html')]),
        ]:
            type = ConvenienceType()
            type.name = convenience_type[0]
            type.save()
            for conv in convenience_type[1]:
                convenience = Convenience()
                convenience.convenience_type = type
                convenience.name = conv[0]
                convenience.file_name = conv[1]
                convenience.save()


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100, verbose_name='Город')),
                ('street', models.CharField(max_length=100, verbose_name='Улица')),
                ('building', models.CharField(max_length=20, verbose_name='Номер дома')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=8, verbose_name='Широта')),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=8, verbose_name='Долгота')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время обновления записи')),
            ],
        ),
        migrations.CreateModel(
            name='ConvenienceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Название категории удобств')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время обновления записи')),
            ],
        ),
        migrations.CreateModel(
            name='RoomCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='Название категории')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время обновления записи')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Наименование помещения')),
                ('square', models.FloatField(max_length=10, verbose_name='Площадь помещения')),
                ('description', models.TextField(verbose_name='Описание')),
                ('payment_per_hour',
                 models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Оплата в час')),
                ('seats_number', models.PositiveIntegerField(verbose_name='Количество рабочих мест')),
                ('minimum_booking_time', models.IntegerField(default=0, verbose_name='Минимальное время аренды')),
                ('start_working_hours', models.TimeField(verbose_name='Время работы помещения с ')),
                ('end_working_hours', models.TimeField(verbose_name='Время завершения работы помещения до ')),
                ('phone_number', models.CharField(max_length=16)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время обновления записи')),
                ('is_active', models.BooleanField(default=False, verbose_name='активна')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_address',
                                              to='createapp.address', verbose_name='Адрес')),
                ('category',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_category',
                                   to='createapp.roomcategory', verbose_name='Категория')),
                ('room_owner',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OfferImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='offer_images', verbose_name='Фото')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_images',
                                           to='createapp.room')),
            ],
        ),
        migrations.CreateModel(
            name='ConvenienceRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_id', models.IntegerField(verbose_name='id помещения')),
                ('convenience_id', models.IntegerField(verbose_name='id удобства')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время обновления записи')),
            ],
            options={
                'unique_together': {('room_id', 'convenience_id')},
            },
        ),
        migrations.CreateModel(
            name='Convenience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Название удобства')),
                ('file_name', models.CharField(max_length=64, verbose_name='Файл ресурса')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время обновления записи')),
                ('convenience_type',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='createapp.conveniencetype',
                                   verbose_name='Категория удобств')),
            ],
        ),
        migrations.RunPython(fill_categories),
        migrations.RunPython(fill_convenience),
    ]
