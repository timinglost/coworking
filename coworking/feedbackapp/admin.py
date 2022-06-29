from django.contrib import admin
from feedbackapp.models import Contact, QuestionCategory, Question, Message

admin.site.register(Contact)
admin.site.register(QuestionCategory)
admin.site.register(Question)
admin.site.register(Message)