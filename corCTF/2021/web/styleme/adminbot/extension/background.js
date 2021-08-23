const sha1 = async (str) => {
    let buf = new ArrayBuffer(str.length * 2);
    let bufView = new Uint16Array(buf);
    for (let i = 0; i < str.length; i++) {
        bufView[i] = str.charCodeAt(i);
    }

    let hashBuf = await crypto.subtle.digest("SHA-1", buf);
    return [...new Uint8Array(hashBuf)].map(x => x.toString(16).padStart(2, '0')).join('');
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.method === "installCSS" && request.css) {
        let injection = { 
            target: {
                tabId: sender.tab.id
            },
            css: request.css
        };
        if(sender.frameId !== 0) {
            injection.target.frameIds = [sender.frameId];
        }
        chrome.scripting.insertCSS(injection);
    }
    else if(request.method === "sha1" && request.data) {
        sha1(request.data).then(res => sendResponse(res));
    }
    return true;
});

chrome.action.onClicked.addListener((tab) => {
    chrome.runtime.openOptionsPage();
});