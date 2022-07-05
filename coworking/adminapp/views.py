from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from feedbackapp.models import *
from django.urls import reverse
from adminapp.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from createapp.models import *


def check_admin(user):
   return user.is_superuser


def check_admin_staff(user):
   return user.is_staff


@user_passes_test(check_admin_staff)
def room_category_delete(request, pk):
    category = get_object_or_404(RoomCategory, pk=pk)
    category.delete()
    return HttpResponseRedirect(reverse('admin_staff:room_category'))


@user_passes_test(check_admin_staff)
def room_category_add(request):
    title = 'Админка - Категории'
    if request.method == 'POST':
        category_form = RoomCategoryEditForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin_staff:room_category'))
        else:
            return HttpResponseRedirect(reverse('admin_staff:room_category'))
    else:
        category_form = QuestionCategoryEditForm()
    context = {
        'title': title,
        'category_form': category_form
    }
    return render(request, 'adminapp/room_category/room-category-edit.html', context)


@user_passes_test(check_admin_staff)
def room_category_edit(request, pk):
    title = 'Админка - Категории'
    category = get_object_or_404(RoomCategory, pk=pk)
    if request.method == 'POST':
        category_form = RoomCategoryEditForm(request.POST, instance=category)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin_staff:room_category'))
        else:
            return HttpResponseRedirect(reverse('admin_staff:room_category'))
    else:
        category_form = QuestionCategoryEditForm(instance=category)
    context = {
        'title': title,
        'category': category,
        'category_form': category_form
    }
    return render(request, 'adminapp/room_category/room-category-edit.html', context)


@user_passes_test(check_admin_staff)
def room_category(request):
    title = 'Админка - Категории'

    room_category = RoomCategory.objects.all()

    context = {
        'title': title,
        'room_category': room_category
    }
    return render(request, 'adminapp/room_category/room-category.html', context)


@user_passes_test(check_admin_staff)
def allow_publishing(request, pk):
    offer = get_object_or_404(Room, pk=pk)
    if offer.is_active is True:
        offer.is_active = False
        offer.save()
        return HttpResponseRedirect(reverse('admin_staff:offers'))
    else:
        offer.is_active = True
        offer.save()
        return HttpResponseRedirect(reverse('admin_staff:pre_moderation'))


@user_passes_test(check_admin_staff)
def show_offers_details(request, pk):
    offer = get_object_or_404(Room, pk=pk)
    offer_address = get_object_or_404(Address, pk=offer.address.pk)
    category = get_object_or_404(RoomCategory, pk=offer.category.pk)
    # offer_images = offer.prefetch_related('room_images')

    context = {
        'title': offer.name,
        'offer': offer,
        'offer_address': offer_address,
        'category': category,
        # "seats_number": [_ for _ in range(1, offer.seats_number + 1)],
        # 'offer_images': offer_images,
    }
    return render(request, 'adminapp/offers/offers-pm-active.html', context=context)


@user_passes_test(check_admin_staff)
def pre_moderation(request):
    title = 'Админка - Заказы'

    offers_list = Room.objects.filter(is_active=False)

    context = {
        'title': title,
        'offers_list': offers_list
    }
    return render(request, 'adminapp/offers/offers.html', context)


@user_passes_test(check_admin_staff)
def offers(request):
    title = 'Админка - Заказы'

    offers_list = Room.objects.filter(is_active=True)

    context = {
        'title': title,
        'offers_list': offers_list
    }
    return render(request, 'adminapp/offers/offers.html', context)


@user_passes_test(check_admin_staff)
def main(request):
    title = 'Админка'

    context = {
        'title': title,
    }
    return render(request, 'adminapp/index.html', context)


@user_passes_test(check_admin_staff)
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


@user_passes_test(check_admin_staff)
def question_category(request):
    title = 'Админка - F.A.Q.'

    faq_category = QuestionCategory.objects.all()

    context = {
        'title': title,
        'faq_category': faq_category
    }
    return render(request, 'adminapp/faq-category.html', context)


@user_passes_test(check_admin_staff)
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


@user_passes_test(check_admin_staff)
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


@user_passes_test(check_admin_staff)
def delete_category(request, pk):
    category = get_object_or_404(QuestionCategory, pk=pk)
    category.delete()
    return HttpResponseRedirect(reverse('admin_staff:question_category'))


@user_passes_test(check_admin_staff)
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


@user_passes_test(check_admin_staff)
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


@user_passes_test(check_admin_staff)
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


@user_passes_test(check_admin_staff)
def question_delete(request, pk_cat, pk):
    question = get_object_or_404(Question, pk=pk)
    question.delete()
    return HttpResponseRedirect(reverse('admin_staff:questions', kwargs={'pk': pk_cat}))


@user_passes_test(check_admin_staff)
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


@user_passes_test(check_admin_staff)
def get_message(request, pk):
    title = 'Админка - Сообщения'

    message_active = get_object_or_404(Message, pk=pk)

    context = {'title': title,
               'message_active': message_active
               }

    return render(request, 'adminapp/get-message.html', context)


@user_passes_test(check_admin_staff)
def delete_message(request, pk):
    message_active = get_object_or_404(Message, pk=pk)
    message_active.is_active = False
    message_active.save()
    return HttpResponseRedirect(reverse('admin_staff:message'))
