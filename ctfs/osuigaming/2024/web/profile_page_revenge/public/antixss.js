// patented secure anti-xss mechanism™
(() => {
    document.querySelectorAll("meta").forEach(m => m.remove());
    SNOW((win) => {
        const blocked = () => console.log('blocked!');
        win.alert = blocked;
        win.fetch = blocked;
        win.open = blocked;
        win.XMLHttpRequest = blocked;
        win.Document.prototype.createElement = blocked;
        win.Document.prototype.write = blocked;
        win.Navigator.prototype.sendBeacon = blocked;
        win.RTCPeerConnection = blocked;
        win.webkitRTCPeerConnection = blocked;
        win.RTCDataChannel = blocked;
        win.frames = blocked;
        win.URL.createObjectURL = blocked;
        win.setTimeout = blocked;
        win.setInterval = blocked;
        win.WebSocket = blocked;
        win.Worker = blocked;
        win.CustomElementRegistry.prototype.define = blocked;
        win.Object.defineProperties = blocked;
        win.Object.defineProperty = blocked;
        win.Object.prototype.__defineGetter__ = blocked;
        win.Object.prototype.__defineSetter__ = blocked;
    });
    window.addEventListener("load", (e) => {
        // freeze the DOM
        const observer = new MutationObserver((mutationsList, observer) => {
            for (const mutation of mutationsList) {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach(node => {
                        if (node.tagName === "META" && node.httpEquiv === "refresh") window.stop();
                        node.remove();
                    });
                } else if (mutation.type === 'attributes') {
                    mutation.target.setAttribute(mutation.attributeName, mutation.oldValue);
                }
            }
        });
        observer.observe(document.documentElement, {
          childList: true,
          subtree: true,
          attributes: true
        });
    });
    console.log("anti-xss loaded!");
})();