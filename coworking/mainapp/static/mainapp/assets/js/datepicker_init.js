function initDatePicker(config){
    config = config ?? {};
    const format = config.format ?? 'DD/MM/YYYY';
    const inputId = config.inputId ?? 'date-range';
    const fromId = config.fromId ?? 'date-from';
    const toId = config.toId ?? 'date-to';

    $(document).ready(() => {

        const initialStart = moment().startOf('day');
        const initialEnd = moment().startOf('day').add(8, 'day');

        const onDateSelected = (start, end, label) => {
            $('#' + fromId).val(start.format(format));
            $('#' + toId).val(end.format(format));
        };

        onDateSelected(initialStart, initialEnd);

        $('#' + inputId).daterangepicker({
            opens: 'left',
            minDate: moment().startOf('day'),
            startDate: initialStart,
            endDate: initialEnd,
             locale: {
              format: format
            }
        }, onDateSelected);
    });
}

