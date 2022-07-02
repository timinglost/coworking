from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from feedbackapp.models import Contact, QuestionCategory, Question, Message
from django.urls import reverse
from adminapp.forms import *
from django.contrib import messages


def main(request):
    title = 'Админка'

    context = {
        'title': title,
    }
    return render(request, 'adminapp/index.html', context)


def edit_contacts(request):
    title = 'Админка - Контакты'
    contacts = Contact.objects.first()
    if request.method == 'POST':
        contact_form = ContactEditForm(request.POST, instance=contacts)
        if contact_form.is_valid():
            contact_form.save()
            return HttpResponseRedirect(reverse('admin_staff:contact'))
        else:
            return HttpResponseRedirect(reverse('admin_staff:contact'))
    else:
        message_form = ContactEditForm(instance=contacts)
    context = {
        'title': title,
        'contacts': contacts,
        'message_form': message_form
    }
    return render(request, 'adminapp/edit_contact.html', context)


def question_category(request):
    title = 'Админка - F.A.Q.'

    faq_category = QuestionCategory.objects.all()

    context = {
        'title': title,
        'faq_category': faq_category
    }
    return render(request, 'adminapp/faq-category.html', context)

def category(request, pk):
    title = 'Админка - F.A.Q.'
    category = get_object_or_404(QuestionCategory, pk=pk)
    if request.method == 'POST':
        category_form = QuestionCategoryEditForm(request.POST, instance=category)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin_staff:question_category'))
        else:
            return HttpResponseRedirect(reverse('admin_staff:question_category'))
    else:
        category_form = QuestionCategoryEditForm(instance=category)
    context = {
        'title': title,
        'category': category,
        'category_form': category_form
    }
    return render(request, 'adminapp/faq-category-edit.html', context)


def add_category(request):
    title = 'Админка - F.A.Q.'
    if request.method == 'POST':
        category_form = QuestionCategoryEditForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin_staff:question_category'))
        else:
            return HttpResponseRedirect(reverse('admin_staff:question_category'))
    else:
        category_form = QuestionCategoryEditForm()
    context = {
        'title': title,
        'category_form': category_form
    }
    return render(request, 'adminapp/faq-category-edit.html', context)


def delete_category(request, pk):
    category = get_object_or_404(QuestionCategory, pk=pk)
    category.delete()
    return HttpResponseRedirect(reverse('admin_staff:question_category'))


def questions(request, pk):
    title = 'Админка - F.A.Q.'
    faq_category = get_object_or_404(QuestionCategory, pk=pk)
    faq_question = Question.objects.filter(category__pk=pk)
    context = {
        'title': title,
        'faq_category': faq_category,
        'faq_question': faq_question
    }
    return render(request, 'adminapp/faq-questions.html', context)


def question_edit(request, pk_cat, pk):
    title = 'Админка - F.A.Q.'
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        question_form = QuestionEditForm(request.POST, instance=question)
        if question_form.is_valid():
            question_form.save()
            return HttpResponseRedirect(reverse('admin_staff:questions', kwargs={'pk': pk_cat}))
        else:
            return HttpResponseRedirect(reverse('admin_staff:questions', kwargs={'pk': pk_cat}))
    else:
        question_form = QuestionEditForm(instance=question)
    context = {
        'title': title,
        'question': question,
        'question_form': question_form
    }
    return render(request, 'adminapp/faq-question-edit.html', context)


def question_add(request, pk_cat):
    title = 'Админка - F.A.Q.'
    faq_category = get_object_or_404(QuestionCategory, pk=pk_cat)
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        try:
            Question.objects.get(slug=slug)
            messages.info(request, 'Такой slug уже существует!')
            return HttpResponseRedirect(reverse('admin_staff:question_add', kwargs={'pk_cat': pk_cat}))
        except:
            text = request.POST.get('text')
            new_question = Question(category=faq_category, name=name, slug=slug, text=text)
            new_question.save()
            return HttpResponseRedirect(reverse('admin_staff:questions', kwargs={'pk': pk_cat}))
    context = {
        'title': title,
        'faq_category': faq_category,
    }
    return render(request, 'adminapp/faq-question-add.html', context)


def question_delete(request, pk_cat, pk):
    question = get_object_or_404(Question, pk=pk)
    question.delete()
    return HttpResponseRedirect(reverse('admin_staff:questions', kwargs={'pk': pk_cat}))


def message(request):
    title = 'Админка - Сообщения'

    messages_active = Message.objects.filter(is_active=True)
    messages_not_active = Message.objects.filter(is_active=False)

    context = {
        'title': title,
        'messages_active': messages_active,
        'messages_not_active': messages_not_active
    }
    return render(request, 'adminapp/messages.html', context)


def get_message(request, pk):
    title = 'Админка - Сообщения'

    message_active = get_object_or_404(Message, pk=pk)

    context = {'title': title,
               'message_active': message_active
               }

    return render(request, 'adminapp/get-message.html', context)


def delete_message(request, pk):
    message_active = get_object_or_404(Message, pk=pk)
    message_active.is_active = False
    message_active.save()
    return HttpResponseRedirect(reverse('admin_staff:message'))