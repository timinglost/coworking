window.onload = function () {
    var times = document.querySelector('.times')
    var start_date = document.querySelector('input[id=start_date]')
    var end_date = document.querySelector('input[id=end_date]')
    var fromEl = document.querySelector('.form-control')

    var start_date_val
    var end_date_val

    start_date.addEventListener('change', function (event) {
            start_date_val = event.target.value;
            console.log(start_date_val);
            CompareDates(start_date_val, end_date_val);
        });

    end_date.addEventListener('change', function (event) {
            end_date_val = event.target.value;
            console.log(end_date_val);
            CompareDates(start_date_val, end_date_val);
        });

    function CompareDates(start_date, end_date) {
        if(start_date==end_date) {
            times.classList.remove('hidden');
        } else{
        times.classList.add('hidden');
        }
    }

}
