function initDatePicker(config){
    config = config ?? {};
    const format = config.format ?? 'YYYY-MM-DD';
    const inputId = config.inputId ?? 'date-range';
    const fromId = config.fromId ?? 'date_from';
    const toId = config.toId ?? 'date_to';

    return new Promise((resolve) => {
        $(document).ready(() => {

            const initialStart = moment().startOf('day');
            const initialEnd = moment().startOf('day').add(8, 'day');


            const onDateSelected = (start, end, label) => {
                $('#' + fromId).val(start.format(format));
                $('#' + toId).val(end.format(format));
            };

            onDateSelected(initialStart, initialEnd);
            const datePicker = $('#' + inputId);
            datePicker.daterangepicker({
                opens: 'left',
                minDate: moment().startOf('day'),
                startDate: initialStart,
                endDate: initialEnd,
                 locale: {
                  format: format
                }
            }, onDateSelected);

            return resolve(datePicker.data('daterangepicker'));
        });
    });

}

