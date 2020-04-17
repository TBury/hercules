$.ajax({
    url: "/process-waybill-api",
    success: function (response) {
        location.href = "/add-waybill"
    },
    error: function () {
        console.log("Wystąpił błąd z połączeniem");
    }
});