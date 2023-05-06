function curl() {
    let url = document.getElementById("url").value;
    let header_key = document.getElementById("header_key").value;
    let header_value = document.getElementById("header_value").value;

    $.ajax({
        type: "GET",
        url: "/curl",
        data : "url=" + url + "&header_key=" + header_key + "&header_value=" + header_value,
        success: (data) => {
            data = JSON.stringify(data)
            document.getElementById("output").value = data
        },
        error: (data) => {
            alert("Something Wrong");
        }
    });
}