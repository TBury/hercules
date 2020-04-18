$.ajax({
    url: "/process-waybill-api",
    success: function (response) {
        location.href = "/add-waybill"
    },
    error: function () {
        toastr.options = {
            toastClass: 'notification is-danger',
        };
        toastr.error("Wystąpił problem z połączeniem. Sprawdź swoje łącze internetowe", "Mamy problem");
    }
});