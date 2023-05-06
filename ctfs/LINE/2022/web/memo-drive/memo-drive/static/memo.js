function save() {
    let contents = document.getElementById("memo-input").value;

    $.ajax({
        type: "GET",
        url: "/save",
        data : "contents=" + contents,
        success: (data) => {
            alert(data);
            location.reload();
        }
    });
}

function reset() {
    $.ajax({
        type: "GET",
        url: "/reset",
        success: (data) => {
            alert(data);
            location.reload();
        }
    });
}