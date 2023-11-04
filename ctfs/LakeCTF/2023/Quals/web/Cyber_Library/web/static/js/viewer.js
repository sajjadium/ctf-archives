let url = new URL(window.location.hash.substring(1));
let schemeSpan = document.getElementById("scheme");
let urlInput = document.getElementById("url-input");
let iframe = document.getElementById("iframe");
schemeSpan.innerText = url.protocol + "//";
urlInput.value = url.hostname + url.pathname + url.search + url.hash;
iframe.src = url;
