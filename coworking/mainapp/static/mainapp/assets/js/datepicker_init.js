function initDatePicker(config){
    config = config ?? {};
    const format = config.format ?? 'DD/MM/YYYY';
    const inputId = config.inputId ?? 'date-range';
    const fromId = config.fromId ?? 'date-from';
    const toId = config.toId ?? 'date-to';
    const autoApply = config.autoApply ?? true;
    const initialFrom = config.initialStart ?? moment().startOf('day');
    const initialTo = config.initialEnd ?? moment().startOf('day').add(8, 'day');

    return new Promise((resolve) => {
        $(document).ready(() => {

            const initialStart = initialFrom;
            const initialEnd = initialTo;

            const onDateSelected = (start, end, label) => {
                $('#' + fromId).val(typeof start === 'string' ? start : start.format(format));
                $('#' + toId).val(typeof end === 'string' ? end : end.format(format));
            };

            onDateSelected(initialStart, initialEnd);
            const datePicker = $('#' + inputId);
            datePicker.daterangepicker({
                opens: 'left',
                autoApply: autoApply,
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

