ymaps.ready(init);


let check_was_done = false;

function onNewAd(event){
    if(check_was_done) {
        check_was_done = false;
        return;
    }
    event.preventDefault();
    const address = $('#address').val();

    if(!address){
        showError('Address must not be empty');
        return;
    }

    checkAddress(address)
        .then(result => {
            if(result.error){
                showError(result.error);
                return;
            }
            check_was_done = true;
            $(event.srcElement).trigger('click');
        }, err => {
            showError('Internal server error');
        })
}


function showError(message) {
    $('#address-notice').text(message);
    $('#address').addClass('input_error');
    $('#address-notice').css('display', 'block');
}

function clearAddressErrors(){
    $('#address').removeClass('input_error');
    $('#address-notice').css('display', 'none');
}

function init() {
    var suggestView = new ymaps.SuggestView('address');
    $('#address').change(() => clearAddressErrors());
    suggestView.events.add(
        'select',
         e => checkAddress(e.get('item').value)
                .then(result => showResult(result.obj))
     );

    var myPlacemark,
        myMap = new ymaps.Map('map', {
            center: [55.753994, 37.622093],
            zoom: 9
        }, {
            searchControlProvider: 'yandex#search'
        });

    var location = ymaps.geolocation.get();
    location.then(
        result => {
            const coords = result.geoObjects.position;
            myMap.setCenter(coords);
            getAddress(coords);
        }
     );

    // Слушаем клик на карте.
    myMap.events.add('click', function (e) {
        var coords = e.get('coords');
        getPlacemark(coords);
        getAddress(coords);
    });

    // Создание метки.
    function createPlacemark(coords) {
        return new ymaps.Placemark(coords, {
            iconCaption: 'поиск...'
        }, {
            preset: 'islands#violetDotIconWithCaption',
            draggable: true
        });
    }

    // Определяем адрес по координатам (обратное геокодирование).
    function getAddress(coords) {
        getPlacemark(coords).properties.set('iconCaption', 'поиск...');
        ymaps.geocode(coords).then(function (res) {
            var firstGeoObject = res.geoObjects.get(0);
            setPlacemarkText(firstGeoObject);
            $('#address').val(firstGeoObject.getAddressLine());
        });
    }

    function showResult(obj) {
        // Удаляем сообщение об ошибке, если найденный адрес совпадает с поисковым запросом.
        clearAddressErrors();

        var mapContainer = $('#map'),
            bounds = obj.properties.get('boundedBy'),
        // Рассчитываем видимую область для текущего положения пользователя.
            mapState = ymaps.util.bounds.getCenterAndZoom(
                bounds,
                [mapContainer.width(), mapContainer.height()]
            ),
        // Сохраняем полный адрес для сообщения под картой.
            address = [obj.getCountry(), obj.getAddressLine()].join(', '),
        // Сохраняем укороченный адрес для подписи метки.
            shortAddress = [obj.getThoroughfare(), obj.getPremiseNumber(), obj.getPremise()].join(' ');
        // Убираем контролы с карты.
        mapState.controls = [];
        // Создаём карту.
        myMap.setCenter(mapState.center, mapState.zoom);
        myPlacemark = getPlacemark(mapState.center);
        setPlacemarkText(obj);
    }

    function setPlacemarkText(firstGeoObject){
        myPlacemark.properties
                .set({
                    // Формируем строку с данными об объекте.
                    iconCaption: [
                        // Название населенного пункта или вышестоящее административно-территориальное образование.
                        firstGeoObject.getLocalities().length ? firstGeoObject.getLocalities() : firstGeoObject.getAdministrativeAreas(),
                        // Получаем путь до топонима, если метод вернул null, запрашиваем наименование здания.
                        firstGeoObject.getThoroughfare() || firstGeoObject.getPremise()
                    ].filter(Boolean).join(', '),
                    // В качестве контента балуна задаем строку с адресом объекта.
                    balloonContent: firstGeoObject.getAddressLine()
                });
    }

    function getPlacemark(coords){

        if (myPlacemark) {
            myPlacemark.geometry.setCoordinates(coords);
        }
        else {
            myPlacemark = createPlacemark(coords);
            myMap.geoObjects.add(myPlacemark);
            // Слушаем событие окончания перетаскивания на метке.
            myPlacemark.events.add('dragend', function () {
                getAddress(myPlacemark.geometry.getCoordinates());
            });
        }
        return myPlacemark;
    }

}

function checkAddress(address) {
    return ymaps.geocode(address).then(function (res) {
            var obj = res.geoObjects.get(0),
                error, hint;

            if (obj) {
                // Об оценке точности ответа геокодера можно прочитать тут: https://tech.yandex.ru/maps/doc/geocoder/desc/reference/precision-docpage/
                switch (obj.properties.get('metaDataProperty.GeocoderMetaData.precision')) {
                    case 'exact':
                        break;
                    case 'number':
                    case 'near':
                    case 'range':
                        error = 'Неточный адрес, требуется уточнение';
                        hint = 'Уточните номер дома';
                        break;
                    case 'street':
                        error = 'Неполный адрес, требуется уточнение';
                        hint = 'Уточните номер дома';
                        break;
                    case 'other':
                    default:
                        error = 'Неточный адрес, требуется уточнение';
                        hint = 'Уточните адрес';
                }
            } else {
                error = 'Адрес не найден';
                hint = 'Уточните адрес';
            }

            // Если геокодер возвращает пустой массив или неточный результат, то показываем ошибку.
            return {
                obj: obj,
                error: error,
                hint: hint
            };
        });
}