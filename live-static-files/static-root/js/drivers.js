
document.querySelector('.sort_by').addEventListener('change', function () {
    const sortForm = document.querySelector(".sort-form");
    sortForm.submit();
});

let rejectModal = document.querySelector(".reject-modal")
let rejectBackground = document.querySelector(".reject-background")
let rejectCloseButton = document.querySelector(".reject-close")

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

drivers = document.querySelectorAll('.dismiss').forEach(function (driver) {
    driver.addEventListener('click', function () {
     rejectModal.classList.add("is-active");
     driver_id = this.id;
     rejectForm = document.querySelector(".rejectForm");
     rejectForm.action = "/Company/Drivers/DismissDriver/" + driver_id;
    });
})

