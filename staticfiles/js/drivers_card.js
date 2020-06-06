document.querySelector('.change-position').addEventListener('change', function () {
    let select = document.querySelector('.change-position');
    if (select.value == "Szef") {
        let modal = document.getElementById("page-modal");
        let modalBackground = document.querySelector(".modal-background")
        let modalCloseButton = document.querySelector(".modal-close")
        let cancelButton = document.querySelector(".cancel")

        modal.classList.add("is-active")

        cancelButton.onclick = function () {
            modal.classList.remove("is-active")
            event.stopPropagation();
        }

        modalCloseButton.onclick = function () {
            modal.classList.remove("is-active")
            event.stopPropagation();
        }

        modalBackground.onclick = function () {
            modal.classList.remove("is-active")
            event.stopPropagation();
        }

    }
    else {
        const sortForm = document.querySelector(".change-position-form");
        sortForm.submit();
    }
});