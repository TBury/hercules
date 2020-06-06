let rejectOpenButton = document.querySelector(".reject")
let rejectModal = document.querySelector(".reject-modal")
let rejectBackground = document.querySelector(".reject-background")

let rejectCloseButton = document.querySelector(".reject-close")
let rejectConfirmButton = document.querySelector("#rejectButton")

rejectOpenButton.onclick = function () {
    rejectModal.classList.add("is-active")
}

rejectCloseButton.onclick = function () {
    rejectModal.classList.remove("is-active")
    event.stopPropagation();
}

document.querySelector(".cancel-reject").onclick = function () {
    rejectModal.classList.remove("is-active")
    event.stopPropagation();
}

rejectBackground.onclick = function () {
    rejectModal.classList.remove("is-active")
    event.stopPropagation();
}


let toEditOpenButton = document.querySelector(".to-edit")
let toEditModal = document.querySelector(".toEdit-modal")
let toEditBackground = document.querySelector(".toEdit-background")

let toEditCloseButton = document.querySelector(".toEdit-close")
let toEditConfirmButton = document.querySelector("#toEditButton")

toEditOpenButton.onclick = function () {
    toEditModal.classList.add("is-active")
}

toEditCloseButton.onclick = function () {
    toEditModal.classList.remove("is-active")
    event.stopPropagation();
}

document.querySelector(".cancel-toEdit").onclick = function () {
    toEditModal.classList.remove("is-active")
    event.stopPropagation();
}

toEditBackground.onclick = function () {
    toEditModal.classList.remove("is-active")
    event.stopPropagation();
}
