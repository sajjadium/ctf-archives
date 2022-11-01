// get listing out of path
let houseId = new URL(window.location.href).search
let RELapi = localStorage.getItem("api")

report = function(){ 
    fetch(RELapi + `/report${houseId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
            message: document.getElementById("REL-msg").value
        })}).then((response) => response.json())
        .then((data) => 
        // redirect back to the main page
        window.location.href = `./index.html#${data.msg}`);    
}
