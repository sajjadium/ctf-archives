const $ = document.querySelectorAll.bind(document);

window.addEventListener("load", () => {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has("domain")) $("#domain-search")[0].value = urlParams.get("domain");
    if (urlParams.has("q")) $("#query-search")[0].value = urlParams.get("q");


    const onKeyDown = (evt) => {
        console.log(evt);
        if (evt.key === "Enter") {
            const domain = $("#domain-search")[0].value;
            const query = $("#query-search")[0].value;

            window.location = `/?domain=${encodeURIComponent(domain)}&q=${encodeURIComponent(query)}`;
        }
    }

    $("#domain-search")[0].addEventListener("keydown", onKeyDown)
    $("#query-search")[0].addEventListener("keydown", onKeyDown)
});