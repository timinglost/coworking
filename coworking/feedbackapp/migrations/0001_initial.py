# Generated by Django 4.0.5 on 2022-09-04 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_address', models.TextField(verbose_name='Первый адрес')),
                ('second_address', models.TextField(verbose_name='Второй адрес')),
                ('first_phone', models.CharField(max_length=20, verbose_name='Первый телефон')),
                ('second_phone', models.CharField(max_length=20, verbose_name='Второй телефон')),
                ('first_mail', models.EmailField(max_length=254, verbose_name='Первая почта')),
                ('second_mail', models.EmailField(max_length=254, verbose_name='Вторая почта')),
                ('working_days', models.CharField(max_length=128, verbose_name='Дни работы')),
                ('Opening_hours', models.CharField(max_length=128, verbose_name='Часы работы')),
            ],
            options={
                'verbose_name': 'Контакты',
                'verbose_name_plural': 'Контакты',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='имя пользователя')),
                ('email', models.EmailField(max_length=254, verbose_name='почта')),
                ('subject', models.CharField(max_length=255, verbose_name='тема')),
                ('message', models.TextField(verbose_name='сообщение')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='активна')),
            ],
            options={
                'verbose_name': 'Сообщение от пользователя',
                'verbose_name_plural': 'Сообщения от пользователей',
            },
        ),
        migrations.CreateModel(
            name='QuestionCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='имя')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Категория F.A.Q.',
                'verbose_name_plural': 'Категории - F.A.Q.',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='имя вопроса')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('text', models.TextField(verbose_name='решение проблемы')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedbackapp.questioncategory')),
            ],
            options={
                'verbose_name': 'Вопрос - F.A.Q.',
                'verbose_name_plural': 'Вопросы - F.A.Q.',
            },
        ),
    ]
