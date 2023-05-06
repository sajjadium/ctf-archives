/*
    Secure Storage Service's
    very secure communication method to talk to a sandboxed secure location
*/

window.onload = () => {
    let storage = document.getElementById("secure_storage");
    let user = document.getElementById("user").innerText;
    storage.contentWindow.postMessage(["user", user], storage.src);
};

const changeMsg = () => {
    let storage = document.getElementById("secure_storage");
    storage.contentWindow.postMessage(["localStorage.message", document.getElementById("message").value], storage.src);
};

const changeColor = () => {
    let storage = document.getElementById("secure_storage");
    storage.contentWindow.postMessage(["localStorage.color", document.getElementById("color").value], storage.src);
};