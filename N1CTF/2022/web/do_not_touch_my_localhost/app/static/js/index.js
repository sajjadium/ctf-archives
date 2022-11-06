
function viewNote() {
    const id = this.dataset.id;
    location.href = "/view/"+id;
}

function sendToAdmin() {
    const id = this.dataset.id;
    fetch("/api/sendToAdmin", {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({ id }).toString(),
    }).then(x => x.json()).then(x => {
        if(x.ok === true){
            alert("success")
        }else {
            alert(x.message)
        }
    });
}

function postNote(){
    const content = document.querySelector("#content").value
    fetch("/api/post", {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({ content }).toString(),
    }).then(x => x.json()).then(x => {
        if(x.ok === true){
            location.reload()
        }else {
            alert(x.message)
        }
    });
}

document.querySelectorAll(".view").forEach(e => {
    e.onclick = viewNote
})

document.querySelectorAll(".send").forEach(e => {
    e.onclick = sendToAdmin
})

document.querySelector("#submit").onclick = postNote