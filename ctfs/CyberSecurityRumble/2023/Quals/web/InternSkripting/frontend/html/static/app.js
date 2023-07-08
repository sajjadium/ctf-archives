function work_with_flag(data) {
    console.log(data);
    document.getElementById("flag_target").innerText = data.value;
    document.getElementById("flag_target").classList.remove("error");
}

function show_error(reason){
    document.getElementById("flag_target").innerText = reason;
    document.getElementById("flag_target").classList.add("error");
}

function get_flag() {
    fetch("/api/flag", {
        method: "GET",
        mode: "same-origin",
        cache: "no-cache",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            "X-Coffee-Secret": document.getElementById("flag_secret").value,
        },
        redirect: "follow",
        referrerPolicy: "origin",
    })
        .then((response) => response.json())
        .then((data) => work_with_flag(data))
        .catch((reason) => show_error(reason));
}
