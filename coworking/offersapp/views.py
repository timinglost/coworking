from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView
from django.db.models import Q
from .forms import CreateSearchForm

from createapp.models import Room, Address, RoomCategory  # OfferImages
from createapp.geo_checker import check_address


def get_offers():
    return Room.objects.filter(is_active=True).order_by('payment_per_hour')


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
    title = 'ЛОКАЦИЯ | Каталог помещений'
    # form = CreateSearchForm()
    # if form.is_valid():
    #     try:
    #         address = check_address(form.cleaned_data['address'])
    #         address.save()
    #     except ValidationError as e:
    #         form.add_error('address', e)

    offers_list = get_offers()
    offers_category = {'pk': 0, 'name': 'Все'}
    current_actions = get_actions()
    # paginator = Paginator(offers_list, 5)
    #
    # try:
    #     offers_paginator = paginator.page(page)
    # except PageNotAnInteger:
    #     offers_paginator = paginator.page(1)
    # except EmptyPage:
    #     offers_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': title,
        'offers_list': offers_list,
        # 'offers_list': offers_paginator,
        'offers_category': offers_category,
        'actions': current_actions,
    }

    return render(request, 'offersapp/index.html', context)


class SearchResultsView(ListView):
    model = Room
    template_name = 'offersapp/search_results.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchResultsView, self).get_context_data()
        context['title'] = 'ЛОКАЦИЯ | Поиск помещений'
        context['city'] = self.request.GET.get('City')
        context['min_price'] = self.request.GET.get('min_price')
        context['max_price'] = self.request.GET.get('max_price')
        return context

    def get_queryset(self):
        city = self.request.GET.get('City')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

        min_price = int(min_price) if min_price else 0
        max_price = int(max_price) if max_price else 10 ** 9

        return Room.objects.filter(
            Q(is_active=True),
            Q(address__city__icontains=city),
            Q(payment_per_hour__gte=min_price),
            Q(payment_per_hour__lte=max_price)
        )
