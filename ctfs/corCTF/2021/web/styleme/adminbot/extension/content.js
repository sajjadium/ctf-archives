let stylescripts = [];
let styles = [];

chrome.storage.local.get('stylescripts', async (result) => {
    stylescripts = result.stylescripts || [];
    styles = await Promise.all(stylescripts.map(s => stylescript.parse(s)));

    let active = styles.filter(s => location.href.startsWith(s.url) || s.global);
    let css = active.map(s => s.css).join("\n\n");

    if (css) {
        chrome.runtime.sendMessage({
            method: "installCSS",
            css
        });
    }
});

window.addEventListener("load", async () => {
    let page = document.body.innerText;
    if (page.startsWith("--styleme stylescript v1.0--") && location.href.startsWith("https://styleme.be.ax")) {
        console.log("[styleme] found stylescript on page!");

        let style = await stylescript.parse(page);
        if (styles.map(s => s.hash).includes(style.hash)) {
            return;
        }

        if (!style || style.version !== 1.0 || !style.css || !style.title || (!style.url && !style.global)) {
            return alert("[ERROR] Unable to load this stylescript.")
        }
        let install = true;

        if (install) {
            console.log("[styleme] installing stylescript...");
            stylescripts.push(page);

            chrome.storage.local.set({
                stylescripts
            }, () => {
                try {
                    if(!style.url)
                        return;

                    let url = new URL(style.url);
                    if (url.protocol === "http:" || url.protocol === "https:") {
                        let redir = true;
                        if (redir) {
                            console.log("[styleme] redirecting to stylescript url!");
                            location.href = style.url;
                        }
                    }
                } catch (err) {}
            });
        }
    }
}, false);

// Example stylescript:
/*
--styleme stylescript v1.0--
---------------
title: red background
global: true
version: 1.0
---------------

* {
    background-color: red !important;
}
*/

const stylescript = {};
stylescript.parse = async (content) => {
    let code = {};

    if (!content.startsWith("--styleme stylescript v1.0--\n----")) {
        return;
    }

    let sections = content.split("\n---------------\n").filter(Boolean);
    let metadata = sections[1];
    let css = sections[2]

    for (let line of metadata.split("\n").filter(Boolean)) {
        let split = line.split(":");
        let prop = split[0].trim().toLowerCase(),
            data = split.slice(1).join(":").trim();

        try {
            code[prop] = JSON.parse(data);
        }
        catch(err) {
            code[prop] = data;
        }
    }

    code.css = css.trim();
    code.hash = await sha1(`${code.title}|${code.url}|${code.css}`);
    code.original = content;

    return code;
};

const sha1 = (data) => {
    return new Promise((resolve, reject) => {
        chrome.runtime.sendMessage({
            method: "sha1",
            data
        }, (hash) => {
            resolve(hash);
        });
    });
};