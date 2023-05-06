let ws = new WebSocket("ws://{{ host }}/analytics");

ws.onopen = function (event) {
    console.log("Analytics: Connected to server");
    ws.send(JSON.stringify({
        "client": "analytics",
        "command": "hello",
        "data": {
            "title": document.title,
            "url": document.location.href,
        }
    }));
}

ws.onmessage = function (event) {
    console.log("Analytics: Message received");
    var data = JSON.parse(event.data);
    if (data.command == "send") {
        var nav = window.nav || window.navigator;
        var data = {
            "title": document.title,
            "language": nav.lang,
        }
        console.log("Analytics: Sending data to server");
        window.postMessage(data, "*");
    }
}

ws.onerror = function (event) {
    console.log("Analytics: Error");
    console.log(event);
}

window.addEventListener("message", function (event) {
    var src = document.getElementById("analytics");
    if (src != null) {
        src.innerHTML = "var data = JSON.parse('" + json + "');";
        src.innerHTML += "fetch('/analytics', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data)});";
    }else{
        src = document.createElement("script");
        json = JSON.stringify(event.data);
        src.id = "analytics";
        src.innerHTML = "var data = JSON.parse('" + json + "');";
        src.innerHTML += "fetch('/analytics', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data)});";
        document.body.appendChild(src);
    }
});