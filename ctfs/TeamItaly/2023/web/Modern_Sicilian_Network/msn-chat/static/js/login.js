var SPACES_PORT = 6969; // default value, will be eventually updated later
const PARENT_DOMAIN = location.hostname.substring(location.hostname.indexOf('.')+1);

const logonScreen = document.querySelector("#logon-screen");
const logonHeader = document.querySelector(".logon-header");
const logonForm = document.querySelector(".logon-form");
const logonUser = document.querySelector("input[name=username]");
const logonPass = document.querySelector("input[name=password]");
const propicForm = document.querySelector("#propic-form");
const forgotLink = document.querySelector("a#forgot-password");
const TheButton = document.querySelector("#TheButton");

const loadingScreen = document.querySelector("#loading-screen");
const loadingMessage = document.querySelector("#loading-message");
const errorMessage = document.querySelector("#error-message");

const signinHeader = document.querySelector("#signin-header");
const signupHeader = document.querySelector("#signup-header");
const signinLink = document.querySelector("a#signin");
const signupLink = document.querySelector("a#signup");

const newLocation = (new URLSearchParams(window.location.search)).get("spaces") === null ? "/chat" : `//spaces.${PARENT_DOMAIN}:${SPACES_PORT}/`;

fetch('/api/v1/spacesPort').then(r => r.text()).then(port => SPACES_PORT = port);

function trySession(endpoint, data) {
    return fetch(`/api/v1/${endpoint}`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(data),
    });
}

async function login() {
    loadingMessage.textContent = "Signing in...";
    setStatus(2);
    const res = await trySession("session", {
        "username": logonUser.value,
        "password": logonPass.value
    });
    await new Promise(r => setTimeout(r, 500)); // i just want the MSN animation to be seen
    if (res.ok) {
        window.location.href = newLocation;
    } else {
        setStatus(0);
        errorMessage.textContent = "Login failed.";
    }
}

async function signup() {
    loadingMessage.textContent = "Signing up...";
    setStatus(2);
    const res = await trySession("users", {
        "username": logonUser.value,
        "password": logonPass.value,
        "propic": document.querySelector(".propic-selector [type=radio]:checked").value
    });
    await new Promise(r => setTimeout(r, 1000)); // i just want the MSN animation to be seen
    if (res.ok) {
        window.location.href = newLocation;
    } else {
        setStatus(1);
        if (res.status == 409)
            errorMessage.textContent = "Username already exists.";
        else if (res.status == 400)
            errorMessage.innerHTML = "Registration failed: invalid credentials"
        else
            errorMessage.textContent = "Registration failed: error";
    }
}

var logonStatus = 0;
// 0 = login, 1 = signup, 2 = loading
function setStatus(status) {
    if(status < 0 || status > 2) return;
    logonStatus = status;

    if (status == 0) {
        propicForm.style.display = "none";
        forgotLink.style.display = "inline";
        TheButton.textContent = "Sign in";
    } else if (status == 1) {
        propicForm.style.display = "inline";
        forgotLink.style.display = "none";
        TheButton.textContent = "Sign up";
    }
    logonScreen.style.display = logonStatus != 2 ? "block" : "none";
    signinHeader.style.display = logonStatus == 0 ? "block" : "none";
    signupHeader.style.display = logonStatus == 1 ? "block" : "none";
    errorMessage.style.display = logonStatus != 2 ? "block" : "none";
    loadingScreen.style.display = logonStatus == 2 ? "block" : "none";
}
setStatus(0);

signupLink.onclick = () => setStatus(1);
signinLink.onclick = () => setStatus(0);
forgotLink.onclick = () => alert("Lmao");
logonForm.onsubmit = (e) => {
    e.preventDefault();
    if (logonStatus == 0)
        login();
    else if (logonStatus == 1)
        signup();
    return false;
}