// Initialize all input of type date
const today = new Date();
const minDate = new Date(today.getFullYear(), today.getMonth(), today.getDay()+3);
const options = {
    minDate: minDate,
    showFooter: false,
}

const calendars = bulmaCalendar.attach('[type="datetime"]', options);


const checkbox = document.querySelector("input[name='random-disposition-switch']");
checkbox.addEventListener('change', (event) => {
    if (event.target.checked) {

        fetch('/Dispositions/RandomDisposition')
            .then(response => response.json())
            .then(data => {
                document.querySelector("input[name='loading_city']").innerHTML = data.loading_city;
                document.querySelector("input[name='loading_city']").value = data.loading_city;
                document.querySelector("input[name='unloading_city']").innerHTML = data.unloading_city;
                document.querySelector("input[name='unloading_city']").value = data.unloading_city;
                document.querySelector("input[name='loading_spedition']").innerHTML = data.loading_spedition;
                document.querySelector("input[name='loading_spedition']").value = data.loading_spedition;
                document.querySelector("input[name='unloading_spedition']").innerHTML = data.unloading_spedition;
                document.querySelector("input[name='unloading_spedition']").value = data.unloading_spedition;
                document.querySelector("input[name='cargo']").innerHTML = data.cargo;
                document.querySelector("input[name='cargo']").value = data.cargo;
                document.querySelector("input[name='tonnage']").innerHTML = data.tonnage;
                document.querySelector("input[name='tonnage']").value = data.tonnage;
            });

    }
    else {
        document.querySelector(".newDispositionForm").reset();
    }
})

document.querySelector(".datetimepicker-clear-button").remove()