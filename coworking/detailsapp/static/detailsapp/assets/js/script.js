window.onload = function () {
    var seats = document.querySelector('.select-seats')
    var periods = document.querySelector('.form-peoples')
    var confirm_btn = document.querySelector('.date-btn')
    var date_start = document.querySelector('input[id=start_date]')
    var date_end = document.querySelector('input[id=end_date]')
    var favorite = document.querySelector('.favorite')

    start_date.addEventListener('change', function (event) {
            document.querySelector('.date-btn').classList.add('hidden');
            var current_start_date = new Date(date_start.value).toISOString().split('T')[0];
            var today = new Date().toISOString().split('T')[0];
            if (current_start_date < today) {
                date_start.value = today
            }

            RenderSeats(date_start.value, date_end.value, seats.value);
        });
    end_date.addEventListener('change', function (event) {
            document.querySelector('.date-btn').classList.add('hidden');
            var current_end_date = new Date(date_end.value).toISOString().split('T')[0];
            var today = new Date().toISOString().split('T')[0];
            if (current_end_date < today) {
                date_end.value = today
            }

            RenderSeats(date_start.value, date_end.value, seats.value);
        });
    seats.addEventListener('change', function (event) {
            document.querySelector('.date-btn').classList.add('hidden');
            RenderSeats(date_start.value, date_end.value, seats.value);
    });
    favorite.addEventListener('click', function (event) {
            CheckFavorite(favorite.outerText);

    });


    function RenderSeats(start_date, end_date, seats) {
        if(start_date && end_date && seats) {
            if (start_date > end_date) {
                end_date = start_date;
                date_end.value = start_date;
            }

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
                        document.querySelector('input[id=start_date]').value = date_from;
                        document.querySelector('input[id=end_date]').value = date_to;
                        $.ajax({
                        url: window.location.pathname + date_from + "/" + date_to + "/" + seats + "/",

                        success: function (data) {
                            $('.form-peoples').html(data.result);
                            $(document).ready(function () {
                             $('select.period-select').on('change', function(event){
                                document.querySelector('.date-btn').classList.remove('hidden');
                             })
                            })
                            }

                        })
                    }
                    else{
                        document.querySelector('.date-btn').classList.remove('hidden');
                    }

                });
            });
            },
        });
        }
    }

    function CheckFavorite(text){
        if (text == "В избранное") {
                $.ajax({
                url: window.location.pathname + "add_fav" + "/",

                success: function (data) {
                    $('.short-links-func').html(data.result);
                    $('.favorite').on('click', function(event){
                        CheckFavorite(document.querySelector('.favorite').outerText);
                    });
                }
                })
            } else if (text == "Убрать из избранного"){
                $.ajax({
                url: window.location.pathname + "del_fav" + "/",

                success: function (data) {
                    $('.short-links-func').html(data.result);
                    $('.favorite').on('click', function(event){
                        CheckFavorite(document.querySelector('.favorite').outerText);
                    });
                }
                })

            }
    }
}
