let $games = $('#select-options').selectize({
    maxItems: 5,
    valueField: 'id',
    searchField: 'title',
    options: [{
            id: 1,
            title: 'ATS',
        },
        {
            id: 2,
            title: 'ETS2',
        },
        {
            id: 3,
            title: 'Singleplayer',
        },
        {
            id: 4,
            title: 'Multiplayer',
        },
        {
            id: 5,
            title: 'Promods',
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
    },
    onChange: function (input) {
        let games_input = document.querySelector("#games")
        games_input.value = input;
    }
});


let $dlc = $('#select-dlc').selectize({
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
    },
    onChange: function (input) {
        let dlc_input = document.querySelector("#dlc")
        dlc_input.value = input;
    }
});

document.getElementById("id_logo").onchange = function () {
    var reader = new FileReader();
    reader.onload = function (e) {
        document.querySelector('.company-logo').src = e.target.result;
    };

    reader.readAsDataURL(this.files[0]);
};