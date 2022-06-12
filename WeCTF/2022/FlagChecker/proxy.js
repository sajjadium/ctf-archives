const http2 = require('node-http2');
const fs = require("fs");
const net = require("net");

const proxyHeader = {
    "Server": "Shou's Little H2 Proxy",
    "IFeel": "Lucky",
}

// Load SSL keys
const options = {
    key: fs.readFileSync('certs/server.key'),
    cert: fs.readFileSync('certs/server.crt')
};

// Define routes
const ROUTES = {
    "/": {host: "localhost", port: 10000},
    "/fake_flag": {host: "localhost", port: 10010},
    "/check_flag": {host: "localhost", port: 10010, localOnly: true},
}

// Remove all chars in the headers that can lead to request smuggling
function requestSmugglingFirewall(normalizedKV){
    const normalizedKVLower = normalizedKV.toLowerCase();
    switch (true) {
        case normalizedKVLower.includes("transfer-encoding"):
        case normalizedKVLower.includes("trailers"):
        case normalizedKVLower.includes("keep-alive"):
        case normalizedKVLower.includes("upgrade"):
        case normalizedKVLower.includes("te"):
        case normalizedKVLower.includes("host"):
        case normalizedKVLower.includes("connection"):
        case normalizedKVLower.includes("trailer"):
            return false
    }
    return true
}

// Remove \r\n in the headers
function normalizeHeader(value) {
    return value.replaceAll("\r", "").replaceAll("\n", "")
}

// Remove \r\n and space in path
function normalizePath(value) {
    return value.replaceAll("\r", "")
        .replaceAll("\n", "").replaceAll(" ", "").toLowerCase()
}

// Build a sanitized header
function buildSanitizedHeaders(http2Req){
    let headers = ""
    Object.entries(http2Req.headers).forEach(entry => {
        const [key, value] = entry;
        const normalizedKey = normalizeHeader(key);
        if (requestSmugglingFirewall(normalizedKey)) headers += `${normalizedKey}: ${normalizeHeader(value)}\r\n`
    });
    return headers
}

// Convert HTTP2 to HTTP/1.1
function downgradeReq(http2Req, path){
    return `${http2Req.method} ${path} HTTP/1.1\r\n${buildSanitizedHeaders(http2Req)}\r\n`
}

// Return error
function proxyError(resp, code){
    resp.writeHead(code, "", proxyHeader)
    resp.end("hacker?")
}

// Convert response from HTTP/1.1 to HTTP/2
function respParser(proxyResp){
    let statusCode = 502;
    let headers = {};
    let response = "";
    try {
        let splittedResp = proxyResp.split("\r\n");
        statusCode = parseInt(splittedResp[0].split(" ")[1]);
        let offset = 1;
        for (let i = offset; i < splittedResp.length; i++) {
            if (!splittedResp[i]){
                offset = i + 1
                break
            }
            let headerKV = splittedResp[i].split(": ");
            const normalizedKey = normalizeHeader(headerKV[0]);
            if (requestSmugglingFirewall(normalizedKey))
                headers[normalizedKey] = normalizeHeader(headerKV.slice(1, ).reduce((l,r)=> l+": "+r))
        }
        response = splittedResp[offset] || ""
    } catch (e) { console.log(e) }
    return {statusCode, headers, response}
}

// Return success
function proxySuccess(client, proxyResp){
    const {statusCode, headers, response} = respParser(proxyResp)
    client.writeHead(statusCode, "", headers)
    client.end(response)
}

http2.createServer(options, function(request, response) {
    try {
        setTimeout(function (){
            let serverSocket = new net.Socket();
            serverSocket.setTimeout(8000);
            const requestedPath = normalizePath(request.url);
            const {host, port, localOnly} = ROUTES[requestedPath.split("?")[0]] || {};
            if (!host || !port) return proxyError(response, 404);
            // only localhost can visit
            if (localOnly && request.remoteAddress !== "::ffff:127.0.0.1") return proxyError(response, 403);
            serverSocket.connect(port, host);
            const downgradedReq = downgradeReq(request, requestedPath);
            serverSocket.write(downgradedReq);
            let httpResp = ""
            serverSocket.on('data', function(chunk){ httpResp += chunk });
            serverSocket.on('error', function(){ return proxyError(response, 500) });
            response.on('error', function(){ return proxyError(response, 500) });
            serverSocket.on('timeout', function(){ return proxyError(response, 502) });
            serverSocket.on("end", function(){ return proxySuccess(response, httpResp) })
            serverSocket.on('close', function(hadError) { if (hadError) return proxyError(response, 502) })
            serverSocket.end()
        }, Math.random()*10)  // make 0~10ms delay to prevent timeless timing attack
    } catch (e) {
        console.log(e)
        return proxyError(response, 500)
    }
}).listen(443);

