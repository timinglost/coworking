from createapp.models import Room, OfferImages
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView

from datetime import date
from pprint import pprint

from lxml import html

from .utils import create_url, get_response, validate_data


def get_yandex_news(dom):
    list_of_news = []
    news_list = dom.xpath("//div[contains(@class, 'mg-card_flexible')]")

    for news in news_list:
        news_info = {}

        name_of_the_news = news.xpath(".//a[@class='mg-card__link']/text()")
        news_link = news.xpath(".//a[@class='mg-card__link']/@href")
        news_date = news.xpath(".//span[@class='mg-card-source__time']/text()")
        news_annotation = news.xpath(".//div[@class='mg-card__annotation']/text()")
        news_source = news.xpath(".//a[@class='mg-card__source-link']/text()")
        news_image_link = news.xpath(".//img[contains(@class, 'neo-image')]/@src")
        if len(news_image_link) == 0:
            news_image_link = news.xpath(".//div[contains(@class, 'mg-card__media-block_type_image')]/@style")
            try:
                news_image_link = news_image_link[0]
                news_image_link = news_image_link[news_image_link.find('(') + 1:news_image_link.find(')')]
                news_info['image'] = news_image_link
            except:
                break
        else:
            news_info['image'] = news_image_link[0]

        news_info['source'] = news_source[0]
        news_info['name'] = validate_data(name_of_the_news[0])
        news_info['link'] = news_link[0]
        news_info['date'] = f'{date.today()}T{news_date[0]}+03:00'
        news_info['text'] = news_annotation[0]

        list_of_news.append(news_info)
    return list_of_news


def get_news_data(site):
    url = create_url(site)
    response = get_response(url)
    dom = html.fromstring(response.text)
    news_data = get_yandex_news(dom)

    # pprint(news_data)
    return news_data


def get_offers():
    rooms = Room.objects.filter(is_active=True).order_by('payment_per_hour')
    return rooms


def add_images(rooms):
    offers_dict = {}
    for room in rooms:
        room_images = OfferImages.objects.filter(room=room)
        # room_images = [_ for _ in room_images]
        offers_dict[room] = room_images
    return offers_dict


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

    offers_list = get_offers()
    offers_dict = add_images(offers_list)
    current_actions = get_actions()
    news_list = get_news_data('yandex.ru/news')

    # paginator = Paginator(offers_list, 5)
    #
    # try:
    #     offers_paginator = paginator.page(page)
    # except PageNotAnInteger:
    #     offers_paginator = paginator.page(1)
    # except EmptyPage:
    #     offers_paginator = paginator.page(paginator.num_pages)
    # print(offers_list)

    context = {
        'title': title,
        'offers_list': offers_list,
        # 'offers_list': offers_paginator,
        'actions': current_actions,
        'offers_dict': offers_dict,
        'news_list': news_list,
        # 'form': form,
    }

    return render(request, 'offersapp/index.html', context)


class SearchResultsView(ListView):
    model = Room
    template_name = 'offersapp/search_results.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchResultsView, self).get_context_data()

        offers_dict = add_images(context['object_list'])
        context['offers_dict'] = offers_dict
        context['news_list'] = get_news_data('yandex.ru/news')
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
