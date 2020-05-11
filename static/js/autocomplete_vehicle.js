document.querySelector("#autoCompleteBrand").addEventListener('change', function () {
    createAutoCompleteComponents();
});

function createAutoCompleteComponents() {
    new autoComplete({
        data: { // Data src [Array, Function, Async] | (REQUIRED)
            src: async () => {
                // User search query
                const query = document.querySelector("#autoCompleteBrand").value;
                // Fetch External Data Source
                const source = await fetch("/static/assets/files/vehicles.json");
                // Format data into JSON
                let data = await source.json();
                // Return Fetched data
                for (let i = 0; i < data.length; i++) {
                    if (data[i]["brand"] == query) {
                        data = data[i]["models"];
                        break;
                    }
                }
                return data;
            },
            key: ["model"],
            cache: true
        },
        sort: (a, b) => { // Sort rendered results ascendingly | (Optional)
            if (a.match < b.match) return -1;
            if (a.match > b.match) return 1;
            return 0;
        },
        selector: "#autoCompleteModel", // Input field selector              | (Optional)
        threshold: 1, // Min. Chars length to start Engine | (Optional)
        debounce: 0, // Post duration for engine to start | (Optional)
        searchEngine: "strict", // Search Engine type/mode           | (Optional)
        resultsList: { // Rendered results list object      | (Optional)
            render: true,
            container: source => {
                source.setAttribute("id", "models");
                source.setAttribute("class", "models-containers hidden");

            },
            destination: document.querySelector("#autoCompleteModel"),
            position: "afterend",
            element: "div"
        },
        maxResults: 5, // Max. number of rendered results | (Optional)
        highlight: true, // Highlight matching results      | (Optional)
        resultItem: { // Rendered result item            | (Optional)
            content: (data, source) => {
                source.innerHTML = data.match;
                source.setAttribute("class", "models input");
                document.querySelector(".models-containers").classList.remove("hidden");
            },
            element: "option"
        },
        onSelection: function (feedback) {
            const selection = feedback.selection.value.model;
            document.querySelector("#autoCompleteModel").innerHTML = selection;
            document.querySelector("#autoCompleteModel").setAttribute("value", selection);
            document.querySelector("#autoCompleteModel").value = selection;
            document.querySelector(".models-containers").classList.add("hidden");
            let engines = [];
            for (let j = 0; j < feedback.selection.value.engine.length; j++) {
                engines.push(feedback.selection.value.engine[j]["name"]);
            }
            new autoComplete({
                data: { // Data src [Array, Function, Async] | (REQUIRED)
                    src: engines,
                },
                key: ["name"],
                selector: "#autoCompleteEngine", // Input field selector              | (Optional)
                searchEngine: "strict", // Search Engine type/mode           | (Optional)
                resultsList: { // Rendered results list object      | (Optional)
                    render: true,
                    container: source => {
                        source.setAttribute("id", "engine");
                        source.setAttribute("class", "engine-container hidden");
                    },
                    destination: document.querySelector("#autoCompleteEngine"),
                    position: "afterend",
                    element: "div"
                },
                maxResults: 5, // Max. number of rendered results | (Optional)
                highlight: true, // Highlight matching results      | (Optional)
                resultItem: { // Rendered result item            | (Optional)
                    content: (data, source) => {
                        source.innerHTML = data.match;
                        source.setAttribute("class", "engine input");
                        document.querySelector(".engine-container").classList.remove("hidden");
                    },
                    element: "option"
                },
                onSelection: function (feedback) {
                    const selection = feedback.selection.value;
                    document.querySelector("#autoCompleteEngine").innerHTML = selection;
                    document.querySelector("#autoCompleteEngine").setAttribute("value", selection);
                    document.querySelector("#autoCompleteEngine").value = selection;
                    document.querySelector(".engine-container").classList.add("hidden");
                },
            });
            let chassis = feedback.selection.value.chassis;
            new autoComplete({
                data: { // Data src [Array, Function, Async] | (REQUIRED)
                    src: chassis,
                },
                selector: "#autoCompleteWheelbase", // Input field selector              | (Optional)
                searchEngine: "strict", // Search Engine type/mode           | (Optional)
                resultsList: { // Rendered results list object      | (Optional)
                    render: true,
                    container: source => {
                        source.setAttribute("id", "chassis");
                        source.setAttribute("class", "chassis-container hidden");
                    },
                    destination: document.querySelector("#autoCompleteWheelbase"),
                    position: "afterend",
                    element: "div"
                },
                maxResults: 5, // Max. number of rendered results | (Optional)
                highlight: true, // Highlight matching results      | (Optional)
                resultItem: { // Rendered result item            | (Optional)
                    content: (data, source) => {
                        source.innerHTML = data.match;
                        source.setAttribute("class", "chassis input");
                        document.querySelector(".chassis-container").classList.remove("hidden");
                    },
                    element: "option"
                },
                onSelection: function (feedback) {
                    const selection = feedback.selection.value;
                    document.querySelector("#autoCompleteWheelbase").innerHTML = selection;
                    document.querySelector("#autoCompleteWheelbase").setAttribute("value", selection);
                    document.querySelector("#autoCompleteWheelbase").value = selection;
                    document.querySelector(".chassis-container").classList.add("hidden");
                },
            });
            let cabins = feedback.selection.value.cabin;
            new autoComplete({
                data: { // Data src [Array, Function, Async] | (REQUIRED)
                    src: cabins,
                },
                selector: "#autoCompleteCabin", // Input field selector              | (Optional)
                searchEngine: "strict", // Search Engine type/mode           | (Optional)
                resultsList: { // Rendered results list object      | (Optional)
                    render: true,
                    container: source => {
                        source.setAttribute("id", "cabin");
                        source.setAttribute("class", "cabin-container hidden");
                    },
                    destination: document.querySelector("#autoCompleteCabin"),
                    position: "afterend",
                    element: "div"
                },
                maxResults: 5, // Max. number of rendered results | (Optional)
                highlight: true, // Highlight matching results      | (Optional)
                resultItem: { // Rendered result item            | (Optional)
                    content: (data, source) => {
                        source.innerHTML = data.match;
                        source.setAttribute("class", "cabin input");
                        document.querySelector(".cabin-container").classList.remove("hidden");
                    },
                    element: "option"
                },
                onSelection: function (feedback) {
                    const selection = feedback.selection.value;
                    document.querySelector("#autoCompleteCabin").innerHTML = selection;
                    document.querySelector("#autoCompleteCabin").setAttribute("value", selection);
                    document.querySelector("#autoCompleteCabin").value = selection;
                    document.querySelector(".cabin-container").classList.add("hidden");
                },
            });
            let gearboxes = feedback.selection.value.transmission;
            new autoComplete({
                data: { // Data src [Array, Function, Async] | (REQUIRED)
                    src: gearboxes,
                },
                selector: "#autoCompleteGearbox", // Input field selector              | (Optional)
                searchEngine: "strict", // Search Engine type/mode           | (Optional)
                resultsList: { // Rendered results list object      | (Optional)
                    render: true,
                    container: source => {
                        source.setAttribute("id", "gearbox");
                        source.setAttribute("class", "gearbox-container hidden");
                    },
                    destination: document.querySelector("#autoCompleteGearbox"),
                    position: "afterend",
                    element: "div"
                },
                maxResults: 5, // Max. number of rendered results | (Optional)
                highlight: true, // Highlight matching results      | (Optional)
                resultItem: { // Rendered result item            | (Optional)
                    content: (data, source) => {
                        source.innerHTML = data.match;
                        source.setAttribute("class", "gearbox input");
                        document.querySelector(".gearbox-container").classList.remove("hidden");
                    },
                    element: "option"
                },
                onSelection: function (feedback) {
                    const selection = feedback.selection.value;
                    document.querySelector("#autoCompleteGearbox").innerHTML = selection;
                    document.querySelector("#autoCompleteGearbox").setAttribute("value", selection);
                    document.querySelector("#autoCompleteGearbox").value = selection;
                    document.querySelector(".gearbox-container").classList.add("hidden");
                    
                },
            });
        },
    });
}

createAutoCompleteComponents();