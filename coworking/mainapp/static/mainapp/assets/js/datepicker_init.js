$(document).ready(() => {

    const initialStart = moment().startOf('day');
    const initialEnd = moment().startOf('day').add(8, 'day');

    const onDateSelected = (start, end, label) => {
        $('#date-from').val(start.format('DD/MM/YYYY'));
        $('#date-to').val(end.format('DD/MM/YYYY'));
    };

    onDateSelected(initialStart, initialEnd);

    $('#date-range').daterangepicker({
        opens: 'left',
        minDate: moment().startOf('day'),
        startDate: initialStart,
        endDate: initialEnd,
         locale: {
          format: 'DD/MM/YYYY'
        }
    }, onDateSelected);
});