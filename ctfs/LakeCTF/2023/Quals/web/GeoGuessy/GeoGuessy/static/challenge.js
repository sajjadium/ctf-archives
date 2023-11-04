window.onmessage = function(e){
    window.latitude = e.data.latitude
    window.longitude = e.data.longitude
}

function submitSolution(){
    challId = document.getElementById("challId").innerText
    body = {latitude,longitude,challId}
    fetch("/solveChallenge", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
    }).then(res => res.json()).then(res => {
        if (res != "no"){
            out.innerText = res
        } else {
            out.innerText = "lol no"
        }
    })
}
window.onload = () => {
submitButton.onclick = submitSolution
}