const net = require("net");

backupServerHost = "";
backupServerPort = "";

function sendData(data) {
    const postData = JSON.stringify(data);

    if (data.host != undefined) {
        backupServerHost = data.host;
    }

    if (data.port != undefined) {
        backupServerPort = data.port;
    }

    const options = {
        host: backupServerHost || "localhost",
        port: backupServerPort || "8888",
    };

    if (
        typeof options.host === "string" &&
        options.host.endsWith(".ngrok.io")
    ) {
        const socket = net.connect(options, () => {
            socket.write(postData);
            socket.end();
        });

        socket.on("error", (err) => {
            console.error("Error", err.message);
        });
    }
}

function updateDBs(dataObj, original) {
    let commData = Object.create(dataObj);
    commData["flag"] = "nite{FAKE_FAKE_FAKE_FLAG}";
    commData["log"] = "new entry added";
    sendData(commData);
    return original;
}

module.exports = updateDBs;
