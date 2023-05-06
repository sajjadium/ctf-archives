let stylescripts = [];
chrome.storage.local.get('stylescripts', (result) => {
    stylescripts = result.stylescripts || [];
    listStyles();
});

const listStyles = () => {
    let installed = document.getElementById("installed");

    if (stylescripts.length === 0) {
        installed.innerText = "no stylescripts installed!";
        return;
    }

    for (let style of stylescripts) {
        let div = document.createElement("div");
        div.style.border = "1px solid black";
        div.style.padding = "0.75rem";
        div.style.marginBottom = "1rem";

        let pre = document.createElement("pre");
        let code = document.createElement("code");
        code.innerText = style;
        pre.appendChild(code);
        div.appendChild(pre);

        let btn = document.createElement("button");
        btn.innerText = "Delete";
        btn.onclick = () => {
            let index = stylescripts.indexOf(style);
            stylescripts.splice(index, 1);
            chrome.storage.local.set({
                stylescripts
            }, () => {
                location.reload();
            });
        };
        div.appendChild(btn);

        installed.appendChild(div);
    }
};