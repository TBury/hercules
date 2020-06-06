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

if (showCookie("changed-position") == 'True') {
    showToast('Pomyślnie zmieniono rangę pracownika.', 'Sukces!');
    deleteCookie("changed-position");
}

if (showCookie("waybill_accepted") == 'True') {
    showToast('Pomyślnie zaakceptowano list przewozowy.', 'Akceptacja');
    deleteCookie("waybill_accepted");
}

if (showCookie("waybill_to_edit") == 'True') {
    showToast('Pomyślnie odesłano list przewozowy do poprawki.', 'Odesłany do poprawki');
    deleteCookie("waybill_to_edit");
}

if (showCookie("waybill_rejected") == 'True') {
    showToast('Pomyślnie odrzucono list przewozowy.', 'Odrzucony');
    deleteCookie("waybill_rejected");
}

if (showCookie("information_changed") == 'True') {
    showToast('Pomyślnie zmieniono informacje o firmie.', 'Zmieniono');
    deleteCookie("information_changed");
}

if (showCookie("settings_changed") == 'True') {
    showToast('Pomyślnie zmieniono ustawienia firmy.', 'Zmieniono');
    deleteCookie("settings_changed");
}

if (showCookie("offer_added") == 'True') {
    showToast('Dodano nową ofertę na giełdę zleceń.', 'Dodano ofertę');
    deleteCookie("offer_added");
}

if (showCookie("job_application_accepted") == 'True') {
    showToast('Przyjęto kierowcę do firmy.', 'Przyjęto aplikację');
    deleteCookie("job_applicaton_accepted");
}

if (showCookie("job_application_rejected") == 'True') {
    showToast('Odrzucono aplikację.', 'Przyjęto aplikację');
    deleteCookie("job_applicaton_rejected");
}