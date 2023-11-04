function updateSettings(){
    username = document.getElementsByName("username")[0].value
    body = {username}
    premiumPin = document.getElementsByName("premiumPin")[0].value
    if (premiumPin != "") {
        body.premiumPin = premiumPin
    }
    fetch("/updateUser", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
    }).then(res => res.json()).then(res => {
        if(res == "yes ok"){
            window.location = "/"
        } else {
            alert("plz stop hakk")
        }
    })
}
window.onload = () => {
updateSettingsButton.onclick = updateSettings
}