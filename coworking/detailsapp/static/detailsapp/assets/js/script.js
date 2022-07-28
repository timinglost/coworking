window.onload = function () {
    const datePickerId = '#date-range';

    var seats = document.querySelector('.select-seats');
    var periods = document.querySelector('.form-peoples');
    var confirm_btn = document.querySelector('.date-btn');
    var apply_btn = document.querySelector('.applyBtn');
    var start_date = document.querySelector('input[id=date-from]');
    var end_date = document.querySelector('input[id=date-to]');

    const dataProvider = () => $(datePickerId).data('daterangepicker');
    $(datePickerId).on(
        'apply.daterangepicker',
        (ev, picker) => {
            startDate = picker.startDate.format('YYYY-MM-DD');
            endDate = picker.endDate.format('YYYY-MM-DD');
            renderSeats(startDate, endDate, seats.value, dataProvider);
        }
    );
    seats.addEventListener(
        'change',
        (event) => renderSeats(start_date.value, end_date.value, seats.value, dataProvider)
    );

    function renderSeats(start_date, end_date, seats, dataProvider) {
        console.log(start_date, end_date, seats)
        if(!start_date || !end_date || !seats) {
            return;
        }
        periods.classList.remove('hidden');
        $.ajax({
            url: window.location.pathname + start_date + "/" + end_date + "/" + seats + "/",
            success: (data) => {
                $('.form-peoples').html(data.result);
                $(document).ready(() => {
                    $('#select_period').on('change', (event) => {
                        var dates = event.target.selectedOptions[0].innerText;
                        if (!isNaN(dates)) {
                            return;
                        }
                        var selected_dates = dates.matchAll(/\d{2}\/\d{2}\/\d\d\d\d/g);
                        selected_dates = Array.from(selected_dates)
                        var date_from = selected_dates[0][0].split('/').reverse().join('-');
                        var date_to = selected_dates[1][0].split('/').reverse().join('-');
                        const datePickerData = dataProvider();
                        datePickerData.setStartDate(date_from);
                        datePickerData.setEndDate(date_to);
                        document.querySelector('.date-btn').classList.remove('hidden');
//                        $.ajax({
//                            url: window.location.pathname + document.querySelector('input[id=date-from]').value + "/" + document.querySelector('input[id=date-to]').value + "/" + seats + "/",
//                            success: (data) => $('.form-peoples').html(data.result)
//                        })
                    });
                });
            },
        });
    }
}
