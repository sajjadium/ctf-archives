const reqButton = document.getElementById("req");
const reqData = document.getElementById("req-data");
const reqInput = document.getElementById("req-input");
const signButton = document.getElementById("sign");
const signData = document.getElementById("sign-data");
const signInput = document.getElementById("sign-input");
const flagButton = document.getElementById("flag");
const flagData = document.getElementById("flag-data");

const decoder = new TextDecoder("utf-8");

reqButton.onclick = async () => {
    let challenge = await (await fetch("req")).arrayBuffer();
    challenge = decoder.decode(challenge);

    reqData.innerText = challenge;
    reqInput.disabled = false;
    signButton.disabled = false;
}

signButton.onclick = async () => {
    if (signButton.disabled) {
        return;
    }
    let signature = await (await fetch("sign?" + reqInput.value)).arrayBuffer();
    signature = decoder.decode(signature);

    signData.innerText = signature;
    signInput.disabled = false;
    flagButton.disabled = false;
}

flagButton.onclick = async () => {
    if (flagButton.disabled) {
        return;
    }

    let flag = await (await fetch("flag?" + signInput.value)).arrayBuffer();
    flag = decoder.decode(flag);

    flagData.innerText = flag;
}