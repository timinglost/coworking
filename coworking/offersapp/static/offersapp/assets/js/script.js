ymaps.ready(init);

function init() {

  var address = new ymaps.SuggestView(
    'suggest',
    {provider: provider}
    );

  if (window.location.pathname === '/offers/') {
        ChangeURL();
  };

  ymaps.geocode(address.state.get('request'), {
        results: 1
    }).then(function (res) {
            // Выбираем первый результат геокодирования.
            var firstGeoObject = res.geoObjects.get(0),
                // Координаты геообъекта.
                coords = firstGeoObject.geometry.getCoordinates(),
                // Область видимости геообъекта.
                bounds = firstGeoObject.properties.get('boundedBy');

            firstGeoObject.options.set('preset', 'islands#darkBlueDotIconWithCaption');
            // Получаем строку с адресом и выводим в иконке геообъекта.
            firstGeoObject.properties.set('iconCaption', firstGeoObject.getAddressLine());

            // Добавляем первый найденный геообъект на карту.
            myMap.geoObjects.add(firstGeoObject);
            // Масштабируем карту на область видимости геообъекта.
            myMap.setBounds(bounds, {
                // Проверяем наличие тайлов на данном масштабе.
                checkZoomRange: true
            });

            /**
             * Все данные в виде javascript-объекта.
             */
//            console.log('Все данные геообъекта: ', firstGeoObject.properties.getAll());
            /**
             * Метаданные запроса и ответа геокодера.
             * @see https://api.yandex.ru/maps/doc/geocoder/desc/reference/GeocoderResponseMetaData.xml
             */
//            console.log('Метаданные ответа геокодера: ', res.metaData);
            /**
             * Метаданные геокодера, возвращаемые для найденного объекта.
             * @see https://api.yandex.ru/maps/doc/geocoder/desc/reference/GeocoderMetaData.xml
             */
//            console.log('Метаданные геокодера: ', firstGeoObject.properties.get('metaDataProperty.GeocoderMetaData'));
            /**
             * Точность ответа (precision) возвращается только для домов.
             * @see https://api.yandex.ru/maps/doc/geocoder/desc/reference/precision.xml
             */
//            console.log('precision', firstGeoObject.properties.get('metaDataProperty.GeocoderMetaData.precision'));
            /**
             * Тип найденного объекта (kind).
             * @see https://api.yandex.ru/maps/doc/geocoder/desc/reference/kind.xml
             */
//            console.log('Тип геообъекта: %s', firstGeoObject.properties.get('metaDataProperty.GeocoderMetaData.kind'));
//            console.log('Название объекта: %s', firstGeoObject.properties.get('name'));
//            console.log('Описание объекта: %s', firstGeoObject.properties.get('description'));
//            console.log('Полное описание объекта: %s', firstGeoObject.properties.get('text'));
            /**
            * Прямые методы для работы с результатами геокодирования.
            * @see https://tech.yandex.ru/maps/doc/jsapi/2.1/ref/reference/GeocodeResult-docpage/#getAddressLine
            */
//            console.log('\nГосударство: %s', firstGeoObject.getCountry());
//            console.log('Населенный пункт: %s', firstGeoObject.getLocalities().join(', '));
//            console.log('Адрес объекта: %s', firstGeoObject.getAddressLine());
//            console.log('Наименование здания: %s', firstGeoObject.getPremise() || '-');
//            console.log('Номер здания: %s', firstGeoObject.getPremiseNumber() || '-');

            /**
             * Если нужно добавить по найденным геокодером координатам метку со своими стилями и контентом балуна, создаем новую метку по координатам найденной и добавляем ее на карту вместо найденной.
             */
            /**
             var myPlacemark = new ymaps.Placemark(coords, {
             iconContent: 'моя метка',
             balloonContent: 'Содержимое балуна <strong>моей метки</strong>'
             }, {
             preset: 'islands#violetStretchyIcon'
             });

             myMap.geoObjects.add(myPlacemark);
             */
        });

  var myPlacemark,
        myMap = new ymaps.Map('map', {
            center: [55.753994, 37.622093],
            zoom: 9
        }, {
            searchControlProvider: 'yandex#search'
        });


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
    };

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

var provider = {
  suggest :  function(request, options) {
    var resultArray = [];
    var suggest = new ymaps.suggest(request);
    var result = suggest.then( items => {
      for (const i of items) {
        resultArray.push({
          value: i.value.split(',').pop().replace(/\s+/g, ''),
          displayName: i.displayName.split(',').slice(0,2)
        });
      }

      return ymaps.vow.resolve(resultArray);
    });
        return ymaps.vow.resolve(result);
  }
};

function clearForm(oForm) {

  var elements = oForm.elements;
  oForm.reset();

  var searchParams = new URLSearchParams(document.location.search);

  for(i=0; i<elements.length; i++) {

    field_type = elements[i].type.toLowerCase();

    switch(field_type) {

		case "text":
		case "password":
		case "textarea":
	    case "hidden":
	        if (searchParams.has(elements[i].name)) {
	            searchParams.delete(elements[i].name)
	        }
			elements[i].defaultValue = "";
			break;

		case "radio":
		case "checkbox":
  			if (elements[i].checked) {
                if (searchParams.has(elements[i].name)) {
                    searchParams.delete(elements[i].name)
                }
   				elements[i].defaultChecked = false;
			}
			break;

		case "select-one":
		case "select-multi":
		    if (searchParams.has(elements[i].name)) {
	            searchParams.delete(elements[i].name)
	        }
            		elements[i].selectedIndex = -1;
			break;

		default:
			break;
	}
    }
    window.history.replaceState({}, '', `${location.pathname}?${searchParams}`);
    location.reload()
};

const formElement = document.getElementById('citySearchForm'); // извлекаем элемент формы
formElement.addEventListener('submit', (e) => {
  e.preventDefault();
  const formData = new FormData(formElement); // создаём объект FormData, передаём в него элемент формы
  // теперь можно извлечь данные
  const newCity = formData.get('City');
  var urlPathname = document.location.pathname;
  var searchOption = 'search/';
  if (urlPathname.indexOf(searchOption) === -1) {
    window.history.replaceState({}, '', `${location.pathname}${searchOption}`)
  }

  var searchParams = new URLSearchParams(document.location.search);
  searchParams.set('City', newCity);
  window.history.replaceState({}, '', `${location.pathname}?${searchParams}`);
  location.reload()

});

const mainFormElement = document.getElementById('searchForm'); // извлекаем элемент формы
mainFormElement.addEventListener('submit', (e) => {
    e.preventDefault();
    var searchParams = new URLSearchParams(document.location.search)

    var elements = mainFormElement.elements;

    for(i=0; i<elements.length; i++) {
        if (elements[i].type.toLowerCase() === 'checkbox') {
            if (elements[i].checked) {
                searchParams.set(elements[i].name, elements[i].value)
			}
			else {
			    searchParams.delete(elements[i].name)
			}
		}
        else {
            searchParams.set(elements[i].name, elements[i].value)
        }
    }
    window.history.replaceState({}, '', `${location.pathname}?${searchParams}`);
    location.reload()
});

function ChangeURL(userCity) {
    var searchParams = new URLSearchParams(document.location.search);
    searchParams.set('City', 'Москва');
    var newPathname = '/offers/search/'
    window.history.replaceState({}, '', `${newPathname}?${searchParams}`);
    location.reload();
};
