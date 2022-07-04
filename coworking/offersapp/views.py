from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from createapp.models import Room, Address, RoomCategory


def get_offers():
    # return Room.objects.all()
    return Room.objects.filter(is_active=False).order_by('payment_per_hour')


def get_actions():
    '''
    функция получения акций для посетителей
    '''
    actions = {
        'name': 'Скидка первым посетителям',
        'text': 'В июле первые 10 заказчиков получат скидку за аренду 25%',
    }
    return actions


def main(request, page=1):
    title = 'ЛОКАЦИЯ | Поиск помещений'

    offers_list = get_offers()
    offers_category = {'pk': 0, 'name': 'Все'}
    current_actions = get_actions()
    paginator = Paginator(offers_list, 2)

    try:
        offers_paginator = paginator.page(page)
    except PageNotAnInteger:
        offers_paginator = paginator.page(1)
    except EmptyPage:
        offers_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': title,
        'offers_list': offers_paginator,
        'offers_category': offers_category,
        'actions': current_actions,
    }

    return render(request, 'offersapp/index.html', context)
