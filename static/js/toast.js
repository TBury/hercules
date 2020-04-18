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


function showToast(toastText, toastTitle) {
    $(document).ready(function () {
        toastr.options = {
            toastClass: 'notification is-success',
        };
        toastr.success(toastText, toastTitle);
    });
}

if (showCookie("waybill_success") == 'True')   {
    showToast('Poprawnie dodano nowy list przewozowy. Statystyki zostaną zaktualizowane po zatwierdzeniu przez spedycję.', 'Sukces!');
    deleteCookie("waybill_success");
}

if (showCookie("vehicle_added") == 'True') {
    showToast('Poprawnie dodano nowy pojazd. Życzymy niezawodności i milionów kilometrów!', 'Sukces!');
    deleteCookie("vehicle_added");
}

if (showCookie("vehicle_deleted") == 'True') {
    showToast('Pojazd został poprawnie usunięty.', 'Pojazd usunięty');
    deleteCookie("vehicle_deleted");
}

if (showCookie("vehicle_edited") == 'True') {
    showToast('Poprawnie edytowano dane pojazdu.', 'Sukces!');
    deleteCookie("vehicle_edited");
}

if (showCookie("dispose_offer_success") == 'True') {
    showToast('Przydzielono ofertę z giełdy zleceń. Znajdziesz ją w panelu Dyspozycje. Szerokości!', 'Sukces!');
    deleteCookie("dispose_offer_success");
}


