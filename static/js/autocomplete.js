new autoComplete({
    data: {                              // Data src [Array, Function, Async] | (REQUIRED)
      src: async () => {
        // User search query
        const query = document.querySelector("#autoCompleteCities").value;
        // Fetch External Data Source
        const source = await fetch("/static/assets/files/companies.json");
        // Format data into JSON
        const data = await source.json();
        // Return Fetched data
        return data;
      },
      key: ["city_name"],
      cache: true
    },
    sort: (a, b) => {                    // Sort rendered results ascendingly | (Optional)
        if (a.match < b.match) return -1;
        if (a.match > b.match) return 1;
        return 0;
    },
    selector: "#autoCompleteCities",           // Input field selector              | (Optional)
    threshold: 1,                        // Min. Chars length to start Engine | (Optional)
    debounce: 0,                       // Post duration for engine to start | (Optional)
    searchEngine: "strict",              // Search Engine type/mode           | (Optional)
    resultsList: {                       // Rendered results list object      | (Optional)
        render: true,
        container: source => {
            source.setAttribute("id", "cities");
            source.setAttribute("class", "cities-container hidden");
        },
        destination: document.querySelector("#autoCompleteCities"),
        position: "afterend",
        element: "div"
    },
    maxResults: 5,                         // Max. number of rendered results | (Optional)
    highlight: true,                       // Highlight matching results      | (Optional)
    resultItem: {                          // Rendered result item            | (Optional)
        content: (data, source) => {
            source.innerHTML = data.match;
            source.setAttribute("class", "city input");
            document.querySelector(".cities-container").classList.remove("hidden");
        },
        element: "option"
    },
    onSelection: function (feedback) {
        const selection = feedback.selection.value.city_name;
        document.querySelector("#autoCompleteCities").innerHTML = selection;
        document.querySelector("#autoCompleteCities").setAttribute("value", selection);
        document.querySelector("#autoCompleteCities").value = selection;
        document.querySelector(".cities-container").classList.add("hidden");
        let loadingCompanies = feedback.selection.value.companies;
        new autoComplete({
            data: { // Data src [Array, Function, Async] | (REQUIRED)
                src: loadingCompanies,
            },
            selector: "#autoCompleteSpedition", // Input field selector              | (Optional)
            searchEngine: "strict", // Search Engine type/mode           | (Optional)
            resultsList: { // Rendered results list object      | (Optional)
                render: true,
                container: source => {
                    source.setAttribute("id", "spedition");
                    source.setAttribute("class", "company-container hidden");
                },
                destination: document.querySelector("#autoCompleteSpedition"),
                position: "afterend",
                element: "div"
            },
            maxResults: 5, // Max. number of rendered results | (Optional)
            highlight: true, // Highlight matching results      | (Optional)
            resultItem: { // Rendered result item            | (Optional)
                content: (data, source) => {
                    source.innerHTML = data.match;
                    source.setAttribute("class", "spedition input");
                    document.querySelector(".company-container").classList.remove("hidden");
                },
                element: "option"
            },
            onSelection: function (feedback) {
                const selection = feedback.selection.value;
                document.querySelector("#autoCompleteSpedition").innerHTML = selection;
                document.querySelector("#autoCompleteSpedition").setAttribute("value", selection);
                document.querySelector("#autoCompleteSpedition").value = selection;
                document.querySelector(".company-container").classList.add("hidden");
            },
        });
        // document.querySelector("#id_loading_country").innerHTML = feedback.selection.value.country;
        // document.querySelector("#id_loading_country").setAttribute("value", feedback.selection.value.country);
    },
});

new autoComplete({
    data: { // Data src [Array, Function, Async] | (REQUIRED)
        src: async () => {
            // User search query
            const query = document.querySelector("#autoCompleteUnloadingCities").value;
            // Fetch External Data Source
            const source = await fetch("/static/assets/files/companies.json");
            // Format data into JSON
            const data = await source.json();
            // Return Fetched data
            return data;
        },
        key: ["city_name"],
        cache: true
    },
    sort: (a, b) => { // Sort rendered results ascendingly | (Optional)
        if (a.match < b.match) return -1;
        if (a.match > b.match) return 1;
        return 0;
    },
    selector: "#autoCompleteUnloadingCities", // Input field selector              | (Optional)
    threshold: 1, // Min. Chars length to start Engine | (Optional)
    debounce: 0, // Post duration for engine to start | (Optional)
    searchEngine: "strict", // Search Engine type/mode           | (Optional)
    resultsList: { // Rendered results list object      | (Optional)
        render: true,
        container: source => {
            source.setAttribute("id", "unloading-cities");
            source.setAttribute("class", "unloading-cities-container hidden");
        },
        destination: document.querySelector("#autoCompleteUnloadingCities"),
        position: "afterend",
        element: "div"
    },
    maxResults: 5, // Max. number of rendered results | (Optional)
    highlight: true, // Highlight matching results      | (Optional)
    resultItem: { // Rendered result item            | (Optional)
        content: (data, source) => {
            source.innerHTML = data.match;
            source.setAttribute("class", "city input");
            document.querySelector(".unloading-cities-container").classList.remove("hidden");
        },
        element: "option"
    },
    onSelection: function (feedback) {
        const selection = feedback.selection.value.city_name;
        document.querySelector("#autoCompleteUnloadingCities").innerHTML = selection;
        console.log(selection);
        document.querySelector("#autoCompleteUnloadingCities").setAttribute("value", selection);
        document.querySelector("#autoCompleteUnloadingCities").value = selection;
        document.querySelector(".unloading-cities-container").classList.add("hidden");
        let unloadingCompanies = feedback.selection.value.companies;
        new autoComplete({
            data: { // Data src [Array, Function, Async] | (REQUIRED)
                src: unloadingCompanies,
            },
            selector: "#autoCompleteUnloadingSpedition", // Input field selector              | (Optional)
            searchEngine: "strict", // Search Engine type/mode           | (Optional)
            resultsList: { // Rendered results list object      | (Optional)
                render: true,
                container: source => {
                    source.setAttribute("id", "unloading-spedition");
                    source.setAttribute("class", "unloading-company-container hidden");
                },
                destination: document.querySelector("#autoCompleteUnloadingSpedition"),
                position: "afterend",
                element: "div"
            },
            maxResults: 5, // Max. number of rendered results | (Optional)
            highlight: true, // Highlight matching results      | (Optional)
            resultItem: { // Rendered result item            | (Optional)
                content: (data, source) => {
                    source.innerHTML = data.match;
                    source.setAttribute("class", "unloading-spedition input");
                    document.querySelector(".unloading-company-container").classList.remove("hidden");
                },
                element: "option"
            },
            onSelection: function (feedback) {
                const selection = feedback.selection.value;
                document.querySelector("#autoCompleteUnloadingSpedition").innerHTML = selection;
                document.querySelector("#autoCompleteUnloadingSpedition").setAttribute("value", selection);
                document.querySelector("#autoCompleteUnloadingSpedition").value = selection;
                document.querySelector(".unloading-company-container").classList.add("hidden");
            },
        });
        // document.querySelector("#id_unloading_country").innerHTML = feedback.selection.value.country;
        // document.querySelector("#id_unloading_country").setAttribute("value", feedback.selection.value.country);
    },
});

new autoComplete({
    data: { // Data src [Array, Function, Async] | (REQUIRED)
        src: async () => {
            // User search query
            const query = document.querySelector("#autoCompleteCargo").value;
            // Fetch External Data Source
            const source = await fetch("/static/assets/files/cargo.json");
            // Format data into JSON
            const data = await source.json();
            // Return Fetched data
            return data;
        },
        key: ["cargo_name"],
        cache: true
    },
    sort: (a, b) => { // Sort rendered results ascendingly | (Optional)
        if (a.match < b.match) return -1;
        if (a.match > b.match) return 1;
        return 0;
    },
    selector: "#autoCompleteCargo", // Input field selector              | (Optional)
    threshold: 1, // Min. Chars length to start Engine | (Optional)
    debounce: 0, // Post duration for engine to start | (Optional)
    searchEngine: "strict", // Search Engine type/mode           | (Optional)
    resultsList: { // Rendered results list object      | (Optional)
        render: true,
        container: source => {
            source.setAttribute("id", "cargo");
            source.setAttribute("class", "cargo-container hidden");
        },
        destination: document.querySelector("#autoCompleteCargo"),
        position: "afterend",
        element: "div"
    },
    maxResults: 3, // Max. number of rendered results | (Optional)
    highlight: true, // Highlight matching results      | (Optional)
    resultItem: { // Rendered result item            | (Optional)
        content: (data, source) => {
            source.innerHTML = data.match;
            source.setAttribute("class", "city input")
            document.querySelector(".cargo-container").classList.remove("hidden");
        },
        element: "option"
    },
    onSelection: function (feedback) {
        const selection = feedback.selection.value.cargo_name;
        document.querySelector("#autoCompleteCargo").innerHTML = selection;
        document.querySelector("#autoCompleteCargo").setAttribute("value", selection);
        document.querySelector("#autoCompleteCargo").value = selection;
        document.querySelector("#id_tonnage").value = feedback.selection.value.mass;
        document.querySelector(".cargo-container").classList.add("hidden");
    },
});