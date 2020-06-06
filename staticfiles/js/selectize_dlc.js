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

function showCookie(name) {
    if (document.cookie !== "") {
        const cookies = document.cookie.split(/; */);

        for (let i = 0; i < cookies.length; i++) {
            const cookieName = cookies[i].split("=")[0];
            const cookieVal = cookies[i].split("=")[1];
            if (cookieName === decodeURIComponent(name)) {
                return decodeURIComponent(cookieVal);
            }
        }
    }
}

function deleteCookie(name) {
    const cookieName = encodeURIComponent(name);
    document.cookie = cookieName + "=; expires=Thu, 01 Jan 1970 00:00:01 GMT;";
}

if (showCookie("dlc") != '') {
    let dlc = showCookie("dlc");
    dlc = decodeURIComponent(escape(dlc));
    dlc = dlc.split(/\\054/).join(",")
    let dlc_input = document.querySelector("#select-dlc")
    let selectize = $dlc[0].selectize;
    dlc = Array.from(dlc);
    Array.prototype.forEach.call(dlc, dlc_item => {
        selectize.addItem(dlc_item);
        dlc_input.value += dlc_item + ",";
    });
    deleteCookie("dlc");
}