from createapp.models import Room, OfferImages, Convenience, ConvenienceRoom
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

    return news_data


def get_conveniences():
    return Convenience.objects.all()


def get_offers():
    return Room.objects.filter(is_active=True).order_by('payment_per_hour')


def add_images_info(rooms):
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
    offers_dict = add_images_info(offers_list)
    current_actions = get_actions()
    news_list = get_news_data('yandex.ru/news')
    conveniences_list = get_conveniences()

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
        'conveniences_list': conveniences_list,
        # 'form': form,
    }

    return render(request, 'offersapp/index.html', context)


def get_conveniences_name():
    conveniences = Convenience.objects.values('name')
    conv_names = []
    for elem in conveniences:
        conv_names.append(elem['name'])
    return conv_names


def get_convenience_from_request(request):
    request_list = list(request)
    conv_names = get_conveniences_name()

    requested_conveniences = {}

    for elem in request_list:
        if elem in conv_names:
            conv = list(Convenience.objects.filter(name=elem))[0]
            requested_conveniences[elem] = conv.id

    return requested_conveniences


def get_room_conveniences(room_with_convenience):
    room_conveniences = []
    for elem in room_with_convenience:
        room_conveniences.append(elem.convenience_id)
        # conv = Convenience.objects.filter(id=elem.convenience_id)

    return room_conveniences


class SearchResultsView(ListView):
    model = Room
    template_name = 'offersapp/search_results.html'
    conveniences = get_conveniences()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchResultsView, self).get_context_data()

        offers_dict = add_images_info(context['object_list'])
        context['offers_dict'] = offers_dict
        # context['news_list'] = get_news_data('yandex.ru/news')
        context['title'] = 'ЛОКАЦИЯ | Поиск помещений'
        context['city'] = self.request.GET.get('City')
        context['min_price'] = self.request.GET.get('min_price')
        context['max_price'] = self.request.GET.get('max_price')
        context['conveniences_list'] = self.conveniences

        return context

    def get_queryset(self):
        city = self.request.GET.get('City')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

        min_price = int(min_price) if min_price else 0
        max_price = int(max_price) if max_price else 10 ** 9

        # отфильтруем помещения по городу и стоимости за час
        rooms_filtered_by_city_and_price = Room.objects.filter(
            Q(is_active=True),
            Q(address__city__icontains=city),
            Q(payment_per_hour__gte=min_price),
            Q(payment_per_hour__lte=max_price)
        )

        rooms_filtered_by_city_and_price = [_ for _ in rooms_filtered_by_city_and_price]

        requested_conveniences = get_convenience_from_request(self.request.GET)

        # проверим наличие среди фильтров каких-либо удобств
        if requested_conveniences:
            rooms_filtered_by_conv = []

            for room in rooms_filtered_by_city_and_price:
                room_with_convenience = ConvenienceRoom.objects.filter(room_id=room.id)
                # проверка на наличие в помещениях каких-либо дополнительных удобств
                if room_with_convenience:
                    print(f'room "{room.name}" is in ConvenienceRoom')

                    # сначала получим список с id всех удобств в помещении
                    room_conveniences = get_room_conveniences(room_with_convenience)
                    # теперь проверяем - есть ли в помещении те удобства, которые запросили при поиске
                    if set(requested_conveniences.values()).issubset(room_conveniences):
                        rooms_filtered_by_conv.append(room)

            return rooms_filtered_by_conv

        else:
            return rooms_filtered_by_city_and_price
