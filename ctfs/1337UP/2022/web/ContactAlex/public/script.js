let search = new URLSearchParams(location.search);

// messages
if(search.get("message")) {
    alert(search.get("message"));
    history.replaceState(null, document.title, location.pathname);
}

if($("#main-modal")[0]) {
    $("#close-btn").on("click", () => {
        $("#main-modal").addClass("hide");
    });
}

if($("#report-btn")[0]) {
    $("#report-btn").on("click", () => {
        $("#main-form").attr("action", "/report");
        $("#main-form").submit();
    });
}