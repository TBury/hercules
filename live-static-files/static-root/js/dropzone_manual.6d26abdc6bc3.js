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