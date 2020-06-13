// Initialize all input of type date
const today = new Date();
const minDate = new Date(today.getFullYear(), today.getMonth(), today.getDay() + 3);
const options = {
    dateFormat: "DD/MM/YYYY",
    minDate: minDate,
    showFooter: false,
}

const calendars = bulmaCalendar.attach('[type="datetime"]', options);


const first_checkbox = document.querySelector("input[name='first-random-disposition-switch']");
first_checkbox.addEventListener('change', (event) => {
    if (event.target.checked) {

        fetch('/Dispositions/RandomDisposition')
            .then(response => response.json())
            .then(data => {
                document.querySelector("input[name='first_disposition_form-loading_city']").innerHTML = data.loading_city;
                document.querySelector("input[name='first_disposition_form-loading_city']").value = data.loading_city;
                document.querySelector("input[name='first_disposition_form-unloading_city']").innerHTML = data.unloading_city;
                document.querySelector("input[name='first_disposition_form-unloading_city']").value = data.unloading_city;
                document.querySelector("input[name='first_disposition_form-loading_spedition']").innerHTML = data.loading_spedition;
                document.querySelector("input[name='first_disposition_form-loading_spedition']").value = data.loading_spedition;
                document.querySelector("input[name='first_disposition_form-unloading_spedition']").innerHTML = data.unloading_spedition;
                document.querySelector("input[name='first_disposition_form-unloading_spedition']").value = data.unloading_spedition;
                document.querySelector("input[name='first_disposition_form-cargo']").innerHTML = data.cargo;
                document.querySelector("input[name='first_disposition_form-cargo']").value = data.cargo;
                document.querySelector("input[name='first_disposition_form-tonnage']").innerHTML = data.tonnage;
                document.querySelector("input[name='first_disposition_form-tonnage']").value = data.tonnage;
                document.querySelector("input[name='second_disposition_form-loading_city']").innerHTML = data.unloading_city;
                document.querySelector("input[name='second_disposition_form-loading_city']").value = data.unloading_city;
                document.querySelector("input[name='second_disposition_form-loading_spedition']").innerHTML = data.unloading_spedition;
                document.querySelector("input[name='second_disposition_form-loading_spedition']").value = data.unloading_spedition;
            });

    }
})

const second_checkbox = document.querySelector("input[name='second-random-disposition-switch']");
second_checkbox.addEventListener('change', (event) => {
    if (event.target.checked) {

        fetch('/Dispositions/RandomDisposition')
            .then(response => response.json())
            .then(data => {
                document.querySelector("input[name='second_disposition_form-unloading_city']").innerHTML = data.unloading_city;
                document.querySelector("input[name='second_disposition_form-unloading_city']").value = data.unloading_city;
                document.querySelector("input[name='second_disposition_form-unloading_spedition']").innerHTML = data.unloading_spedition;
                document.querySelector("input[name='second_disposition_form-unloading_spedition']").value = data.unloading_spedition;
                document.querySelector("input[name='second_disposition_form-cargo']").innerHTML = data.cargo;
                document.querySelector("input[name='second_disposition_form-cargo']").value = data.cargo;
                document.querySelector("input[name='second_disposition_form-tonnage']").innerHTML = data.tonnage;
                document.querySelector("input[name='second_disposition_form-tonnage']").value = data.tonnage;
                document.querySelector("input[name='third_disposition_form-loading_city']").innerHTML = data.unloading_city;
                document.querySelector("input[name='third_disposition_form-loading_city']").value = data.unloading_city;
                document.querySelector("input[name='third_disposition_form-loading_spedition']").innerHTML = data.unloading_spedition;
                document.querySelector("input[name='third_disposition_form-loading_spedition']").value = data.unloading_spedition;
            });

    }
})

const third_checkbox = document.querySelector("input[name='third-random-disposition-switch']");
third_checkbox.addEventListener('change', (event) => {
    if (event.target.checked) {

        fetch('/Dispositions/RandomDisposition')
            .then(response => response.json())
            .then(data => {
                document.querySelector("input[name='third_disposition_form-unloading_city']").innerHTML = data.unloading_city;
                document.querySelector("input[name='third_disposition_form-unloading_city']").value = data.unloading_city;
                document.querySelector("input[name='third_disposition_form-unloading_spedition']").innerHTML = data.unloading_spedition;
                document.querySelector("input[name='third_disposition_form-unloading_spedition']").value = data.unloading_spedition;
                document.querySelector("input[name='third_disposition_form-cargo']").innerHTML = data.cargo;
                document.querySelector("input[name='third_disposition_form-cargo']").value = data.cargo;
                document.querySelector("input[name='third_disposition_form-tonnage']").innerHTML = data.tonnage;
                document.querySelector("input[name='third_disposition_form-tonnage']").value = data.tonnage;
                document.querySelector("input[name='fourth_disposition_form-loading_city']").innerHTML = data.unloading_city;
                document.querySelector("input[name='fourth_disposition_form-loading_city']").value = data.unloading_city;
                document.querySelector("input[name='fourth_disposition_form-loading_spedition']").innerHTML = data.unloading_spedition;
                document.querySelector("input[name='fourth_disposition_form-loading_spedition']").value = data.unloading_spedition;
            });

    }
})

const fourth_checkbox = document.querySelector("input[name='fourth-random-disposition-switch']");
fourth_checkbox.addEventListener('change', (event) => {
    if (event.target.checked) {

        fetch('/Dispositions/RandomDisposition')
            .then(response => response.json())
            .then(data => {
                document.querySelector("input[name='fourth_disposition_form-unloading_city']").innerHTML = data.unloading_city;
                document.querySelector("input[name='fourth_disposition_form-unloading_city']").value = data.unloading_city;
                document.querySelector("input[name='fourth_disposition_form-unloading_spedition']").innerHTML = data.unloading_spedition;
                document.querySelector("input[name='fourth_disposition_form-unloading_spedition']").value = data.unloading_spedition;
                document.querySelector("input[name='fourth_disposition_form-cargo']").innerHTML = data.cargo;
                document.querySelector("input[name='fourth_disposition_form-cargo']").value = data.cargo;
                document.querySelector("input[name='fourth_disposition_form-tonnage']").innerHTML = data.tonnage;
                document.querySelector("input[name='fourth_disposition_form-tonnage']").value = data.tonnage;
                document.querySelector("input[name='fifth_disposition_form-loading_city']").innerHTML = data.unloading_city;
                document.querySelector("input[name='fifth_disposition_form-loading_city']").value = data.unloading_city;
                document.querySelector("input[name='fifth_disposition_form-loading_spedition']").innerHTML = data.unloading_spedition;
                document.querySelector("input[name='fifth_disposition_form-loading_spedition']").value = data.unloading_spedition;
            });

    }
})

const fifth_checkbox = document.querySelector("input[name='fifth-random-disposition-switch']");
fifth_checkbox.addEventListener('change', (event) => {
    if (event.target.checked) {

        fetch('/Dispositions/RandomDisposition')
            .then(response => response.json())
            .then(data => {
                document.querySelector("input[name='fifth_disposition_form-unloading_city']").innerHTML = data.unloading_city;
                document.querySelector("input[name='fifth_disposition_form-unloading_city']").value = data.unloading_city;
                document.querySelector("input[name='fifth_disposition_form-unloading_spedition']").innerHTML = data.unloading_spedition;
                document.querySelector("input[name='fifth_disposition_form-unloading_spedition']").value = data.unloading_spedition;
                document.querySelector("input[name='fifth_disposition_form-cargo']").innerHTML = data.cargo;
                document.querySelector("input[name='fifth_disposition_form-cargo']").value = data.cargo;
                document.querySelector("input[name='fifth_disposition_form-tonnage']").innerHTML = data.tonnage;
                document.querySelector("input[name='fifth_disposition_form-tonnage']").value = data.tonnage;
            });

    }
})

document.querySelector(".datetimepicker-clear-button").remove()