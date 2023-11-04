function login(){
    token = document.getElementsByName("token")[0].value
    fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({token})
    }).then(res => res.json()).then(res => {
        if(res == "yes ok"){
            window.location = "/"
        } else {
            alert("plz stop hakk")
        }
    })
}
window.onload = () => {loginButton.onclick = login}