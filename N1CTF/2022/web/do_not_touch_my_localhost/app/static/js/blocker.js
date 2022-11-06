window.proxy_options = null;

window.postMessage({
    type: "setProxy",
    options: {"hostname":"1.2.3.4","port":12345}
}, "*")