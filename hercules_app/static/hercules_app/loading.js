$.ajax({
    url: "http://127.0.0.1:8000/process-waybill-api",
    success: function (response) {
        location.href = "http://127.0.0.1:8000/add-waybill"
    },
    error: function () {
        console.log("Wystąpił błąd z połączeniem");
    }
});