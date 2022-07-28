window.onload = function () {
    var seats = document.querySelector('.select-seats')
    var date_form = document.querySelector('input[id=date-range]')
    var periods = document.querySelector('.form-peoples')
    var confirm_btn = document.querySelector('.date-btn')
    var apply_btn = document.querySelector('.applyBtn')
    var start_date = document.querySelector('input[id=date-from]')
    var end_date = document.querySelector('input[id=date-to]')

    date_form.addEventListener('change', function (event) {
            console.log('change')
            console.log(date_form.value)
            RenderSeats(start_date.value, end_date.value, seats.value);
        });
    seats.addEventListener('change', function (event) {
            RenderSeats(start_date.value, end_date.value, seats.value);
    });


    function RenderSeats(start_date, end_date, seats) {
        console.log(start_date, end_date, seats)
        if(start_date && end_date && seats) {

            periods.classList.remove('hidden');
            $.ajax({
            url: window.location.pathname + start_date + "/" + end_date + "/" + seats + "/",

            success: function (data) {
                $('.form-peoples').html(data.result);
                $(document).ready(function() {
                $('select.period-select').on('change', function(event){
                    var dates = event.target.selectedOptions[0].innerText;
                    if (isNaN(dates)) {
                        var selected_dates = dates.matchAll(/\d{2}\/\d{2}\/\d\d\d\d/g);
                        selected_dates = Array.from(selected_dates)
                        var date_from = selected_dates[0][0].split('/').reverse().join('-');
                        var date_to = selected_dates[1][0].split('/').reverse().join('-');
                        document.querySelector('input[id=date-from]').value = date_from;
                        document.querySelector('input[id=date-to]').value = date_to;
                        document.querySelector('input[id=date-range]').value = date_from + ' - ' + date_to;
                        document.querySelector('.date-btn').classList.remove('hidden');
                        $.ajax({
                        url: window.location.pathname + document.querySelector('input[id=date-from]').value + "/" + document.querySelector('input[id=date-to]').value + "/" + seats + "/",

                        success: function (data) {
                            $('.form-peoples').html(data.result);
                            }
                        })
                    }

                });
            });
            },
        });
        }
    }

}
