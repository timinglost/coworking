window.onload = function () {
    var seats = document.querySelector('.form-peoples')
    var start_date = document.querySelector('input[id=start_date]')
    var end_date = document.querySelector('input[id=end_date]')

    start_date.addEventListener('change', function (event) {
            RenderSeats(start_date.value, end_date.value);
        });

    end_date.addEventListener('change', function (event) {
            RenderSeats(start_date.value, end_date.value);
        });

    function RenderSeats(start_date, end_date) {
        if(start_date && end_date) {

            seats.classList.remove('hidden');
            $.ajax({
            url: window.location.pathname + start_date + "/" + end_date + "/",

            success: function (data) {
                $('.form-peoples').html(data.result);
                $(document).ready(function() {
                $('select.form-select').on('change', function(event){
                    var dates = event.target.selectedOptions[0].innerText;
                    if (isNaN(dates)) {
                        var selected_dates = dates.matchAll(/\d{2}\/\d{2}\/\d\d\d\d/g);
                        selected_dates = Array.from(selected_dates)
                        document.querySelector('input[id=start_date]').value = selected_dates[0][0].split('/').reverse().join('-');
                        document.querySelector('input[id=end_date]').value = selected_dates[1][0].split('/').reverse().join('-');
                        $.ajax({
                        url: window.location.pathname + document.querySelector('input[id=start_date]').value + "/" + document.querySelector('input[id=end_date]').value + "/",

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
