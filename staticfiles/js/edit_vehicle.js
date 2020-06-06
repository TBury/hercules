document.getElementById("id_photo").onchange = function () {
    var reader = new FileReader();
    reader.onload = function (e) {
        document.querySelector('._vehicle-image').src = e.target.result;
    };

    reader.readAsDataURL(this.files[0]);
};