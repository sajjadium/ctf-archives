window.addEventListener("message", function (event) {
  if (event.origin === window.origin) {
    if (event.data.type === "setProxy") {
      let { hostname, port = "1080" } = window.proxy_options ?? event.data.options;
      chrome.runtime.sendMessage({
        type: "setProxy",
        options: { host: hostname, port: parseInt(port) },
      });
    }
  }
});
