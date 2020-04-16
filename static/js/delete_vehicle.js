let modalOpenButton = document.querySelector(".delete-vehicle")
let modal = document.getElementById("page-modal");
let modalBackground = document.querySelector(".modal-background")
let modalCloseButton = document.querySelector(".modal-close")
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
