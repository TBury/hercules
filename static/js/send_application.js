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


$('#select-dlc').selectize({
    maxItems: 7,
    valueField: 'id',
    searchField: 'title',
    options: [{
            id: 1,
            title: 'Going East!',
        },
        {
            id: 2,
            title: 'Skandynawia',
        },
        {
            id: 3,
            title: 'Viva la France',
        },
        {
            id: 4,
            title: 'Italia',
        },
        {
            id: 5,
            title: 'Beyond the Baltic Sea',
        },
        {
            id: 6,
            title: 'Road to the Black Sea',
        },
        {
            id: 7,
            title: 'Iberia',
        },
    ],
    render: {
        option: function (data, escape) {
            return '<div class="option">' +
                '<span class="option-title">' + escape(data.title) + '</span>' +
                '</div>';
        },
        item: function (data, escape) {
            return '<span class="tag is-success">' + escape(data.title) + '</span>';
        }
    },
    create: function (input) {
        return {
            id: 0,
            title: input,
        };
    }
});