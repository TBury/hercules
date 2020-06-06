let modalOpenButton = document.querySelector(".delete-company")
let modal = document.querySelector(".delete-company-modal");
let modalBackground = document.querySelector(".delete-company-background")
let modalCloseButton = document.querySelector(".delete-company-close")
let confirmDeletingButton = document.querySelector("#deleteButton")

modalOpenButton.onclick = function () {
    modal.classList.add("is-active")
}

modalCloseButton.onclick = function () {
    modal.classList.remove("is-active")
    event.stopPropagation();
}

modalBackground.onclick = function () {
    modal.classList.remove("is-active")
    event.stopPropagation();
}

document.getElementById("id_logo").onchange = function () {
    var reader = new FileReader();
    reader.onload = function (e) {
        document.querySelector('.company-logo').src = e.target.result;
    };

    reader.readAsDataURL(this.files[0]);
};