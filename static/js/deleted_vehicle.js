$(document).ready(function () {
    toastr.options = {
        toastClass: 'notification is-danger',
    };
    toastr.success('Pojazd został poprawnie usunięty.', 'Pojazd usunięty');
});