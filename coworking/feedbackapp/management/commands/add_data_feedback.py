from django.core.management.base import BaseCommand
from feedbackapp.models import Contact, QuestionCategory, Question

contact = {
      "first_address": "A108 Adam Street,",
      "second_address": "New York, NY 535022",
      "first_phone": "+1 5589 55488 55",
      "second_phone": "+1 6678 254445 41",
      "first_mail": "info@example.com",
      "second_mail": "contact@example.com",
      "working_days": "Понедельник - Пятница",
      "Opening_hours": "9:00 - 21:00"
    }
category = [
    {
      "name": "Основные"
    },
    {
      "name": "Личные данные"
    },
    {
      "name": "О сайте"
    },
]
questions = [
    {
      "category": 'Основные',
      "name": "Как связаться с тех-поддержкой?",
      "slug": "kak-svezatsa-s-teh-potdderhkoi",
      "text": "Перейдите на страницу \"Контакты\" и свяжитесь с нами через форму отправки сообщения."
    },
    {
      "category": 'Личные данные',
      "name": "Как изменить информацию о себе?",
      "slug": "kak-izmenit-informaciu-o-sebe",
      "text": "Перейдите на страницу профиля и выберете пункт \"Редактировать профиль\"."
    },
    {
      "category": 'Личные данные',
      "name": "Как сменить пароль?",
      "slug": "kak-smenit-parol",
      "text": "Перейдите на страницу профиля и выберете пункт \"Сменить пароль\"."
    },
    {
      "category": "О сайте",
      "name": "Я могу устроиться к вам работать?",
      "slug": "i-mogu-ustroitsa-k-vam-pabotat",
      "text": "Перейдите на страницу контактов и напишите нам сообщение с информацией о себе, кем вы хотите работать и прикрепите ссылку на ваше резюме. В теме сообщения напишите \"Работа\"."
    }
]

class Command(BaseCommand):
    def handle(self, *args, **options):
        Contact.objects.all().delete()
        new_contact = Contact(**contact)
        new_contact.save()
        QuestionCategory.objects.all().delete()
        for el in category:
            new_category = QuestionCategory(**el)
            new_category.save()
        Question.objects.all().delete()
        for question in questions:
            category_name = question['category']
            _category = QuestionCategory.objects.get(name=category_name)
            question['category'] = _category
            new_question = Question(**question)
            new_question.save()
