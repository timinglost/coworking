ymaps.ready(init);

function init() {

    const address = new ymaps.SuggestView('suggest', {provider: provider});

    if (window.location.pathname === '/offers/') {
        ChangeURL();
    };

    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);

    initDatePicker({
        format: 'YYYY-MM-DD',
        initialStart: urlParams.get('date_from'),
        initialEnd: urlParams.get('date_to'),
    });

    ymaps.geocode(address.state.get('request'), {
        results: 1
    }).then((res) => {
            // Выбираем первый результат геокодирования.
            var firstGeoObject = res.geoObjects.get(0),
                coords = firstGeoObject.geometry.getCoordinates(),
                // Область видимости геообъекта.
                bounds = firstGeoObject.properties.get('boundedBy');

            const myMap = new ymaps.Map('map', {
                center: coords,
                zoom: 9
            }, {
                searchControlProvider: 'yandex#search'
            });

            const getDataElement = $('#geo-coords');
            const geoData = JSON.parse(getDataElement.length ? getDataElement.html() : "[]");
            const lats = {
                min: 180,
                max: -180
            };
            const lons = {
                min: 180,
                max: -180
            };
            for(const data of geoData) {
                lats.min = Math.min(lats.min, data.lat);
                lats.max = Math.max(lats.max, data.lat);
                lons.min = Math.min(lons.min, data.lon);
                lons.max = Math.max(lons.max, data.lon);
                myMap.geoObjects.add(
                    new ymaps.Placemark(
                        [data.lat, data.lon],
                        {
                            balloonContentHeader: '<a href = "/details/'+ data.pk + '">' + data.name + '</a>',
                            balloonContent: data.address,
                            hintContent: data.address,
                        }
                    )
                );
            }

            const resultBounds = [
                [Math.max(lats.min, bounds[0][0]), Math.max(lons.min, bounds[0][1])],
                [Math.min(lats.max, bounds[1][0]), Math.min(lons.max, bounds[1][1])]
            ];
            // Масштабируем карту на область видимости геообъекта.
            myMap.setBounds(resultBounds, {
                // Проверяем наличие тайлов на данном масштабе.
                checkZoomRange: true
            });
        });
}

var provider = {
  suggest :  function(request, options) {
    const resultArray = [];
    const suggest = new ymaps.suggest(request);
    return suggest.then( items => {
      for (const i of items) {
        resultArray.push({
          value: i.value.split(',').pop().trim(),
          displayName: i.displayName.split(',').slice(0,2)
        });
      }
      return resultArray;
    });
  }
};

function clearForm(oForm) {

  const elements = oForm.elements;
  oForm.reset();

  const searchParams = new URLSearchParams(document.location.search);

  for(i=0; i<elements.length; i++) {

    field_type = elements[i].type.toLowerCase();

    switch(field_type) {

		case "text":
		case "number":
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
                if (searchParams.has(elements[i].id)) {
                    searchParams.delete(elements[i].id)
                }
   				elements[i].defaultChecked = false;
			}
			break;
        case "range":
            if (searchParams.has(elements[i].id)) {
                        searchParams.delete(elements[i].id)
                    }
            elements[i].defaultValue = "0";
			break;

		case "select-one":
		case "select-multi":
		    if (searchParams.has(elements[i].id)) {
	            searchParams.delete(elements[i].id)
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
  const newCity = formData.get('city');
  var urlPathname = document.location.pathname;
  var searchOption = 'search/';
  if (urlPathname.indexOf(searchOption) === -1) {
    window.history.replaceState({}, '', `${location.pathname}${searchOption}`)
  }

  var searchParams = new URLSearchParams(document.location.search);
  searchParams.set('city', newCity);
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
    searchParams.set('city', 'Москва');
    var newPathname = '/offers/search/'
    window.history.replaceState({}, '', `${newPathname}?${searchParams}`);
    location.reload();
};


function updateTextInput(val) {
          document.getElementById('textInput').value=val;
        };


const collapsedConv = document.querySelectorAll('.conv')
const collapsedCategory = document.querySelectorAll('.category')

const collapseCategoryCountSpan = document.getElementById('collapse_category_count')
const collapseConvCountSpan = document.getElementById('collapse_conv_count')

collapseCategoryCountSpan.innerText=collapsedCategory.length;
collapseConvCountSpan.innerText=collapsedConv.length;

const collapseConvBtn = document.getElementById('collapse_conv')
const collapseCategoryBtn = document.getElementById('collapse_category')

collapseConvBtn.addEventListener('click', function(event){
    if (collapseConvBtn.innerText === 'Скрыть'){
        collapseConvBtn.innerText = `Показать еще ${collapsedConv.length}`
    }
    else {
        collapseConvBtn.innerText = 'Скрыть'
    };
});

collapseCategoryBtn.addEventListener('click', function(event){
    if (collapseCategoryBtn.innerText === 'Скрыть'){
        collapseCategoryBtn.innerText = `Показать еще ${collapsedCategory.length}`
    }
    else {
        collapseCategoryBtn.innerText = 'Скрыть'
    };
});
