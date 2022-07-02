from django.db import migrations, models, transaction


def fill_categories(apps, schema_editor):
    with transaction.atomic():
        RoomCategory = apps.get_model('createapp', 'RoomCategory')
        for cat in ['Open space', 'Office', 'Private office', 'Conference room', 'Video studio']:
            category = RoomCategory()
            category.name = cat
            category.save()


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RoomCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='Название категории')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время обновления записи')),
            ],
        ),
        migrations.RunPython(fill_categories),
    ]
