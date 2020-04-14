Dropzone.options.myDropzone = {
    url: "/Vehicles/AddNewVehicle",
    paramName: "vehicle-photo",
    autoProcessQueue: false,
    maxFiles: 1,
    parallelUploads: 1,
    acceptedFiles: 'image/*',
};

var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});