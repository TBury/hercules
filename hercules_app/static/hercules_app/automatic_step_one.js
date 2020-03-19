Dropzone.options.myDropzone = {
    paramName: "first_screen",
    autoProcessQueue: true,
    maxFiles: 1,
    parallelUploads: 1,

    init: function () {
        myDropzone = this;
        this.on("success", function (response) {
            window.location.href = "/automatic-step-2";
        });
    }
};

Dropzone.options.endScreenDropzone = {
    paramName: "end_screen",
    autoProcessQueue: true,
    maxFiles: 1,
    parallelUploads: 1,

    init: function () {
        endScreenDropzone = this;
        this.on("success", function (response) {
            window.location.href = "/add-waybill";
        });
    }
};