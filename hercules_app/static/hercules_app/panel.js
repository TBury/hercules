$(document).ready(function () {
    toastr.options = {
        toastClass: 'notification is-success',
    };
    toastr.success('Poprawnie dodano nowy list przewozowy. Statystyki zostaną zaktualizowane po zatwierdzeniu przez spedycję.', 'Sukces!');
});