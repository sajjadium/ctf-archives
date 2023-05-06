const { Readability } = require("@mozilla/readability");
const fetch = require("node-fetch");
const express = require("express");
const { JSDOM } = require("jsdom");
const fs = require("fs");

/* flag is in flag.txt */

const PORT = 80;

const app = express();
const http = require('http');
const server = http.createServer(app);
const io = require('socket.io')(server);

app.use(express.static('public'));
app.use(express.json());

let format = (content) => {
    let bootstrap = 'https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css';
    let final = `<body><head><link rel='stylesheet' href='${bootstrap}'></head><body><div class="m-3">${content}</div></body>`;
    return final;
}

io.on('connection', (socket) => {
    socket.on('fetch', async (url) => {
        socket.emit('fetch', await yoink(url));
    });

    socket.on('readerify', async (data) => {
        if(socket.bypass) {
            socket.bypass = false;
            return;
        }

        try {
            let dom = toDOM(data);
            if(!dom) {
                return socket.emit('readerify', format("invalid text!"));
            }

            let article = readerify(dom);
            if(!article) {
                return socket.emit('readerify', format("no text to readerify!"));
            }

            let content = article.content; 

            // if page is part of a series of page, fetch the next page
            let nextDom = await loadNextPage(dom, socket);
            if(nextDom) {
                let nextArticle = readerify(nextDom);
                if(nextArticle) {
                    content += `<hr />` + nextArticle.content;
                }
            }

            return socket.emit('readerify', format(content));
        }
        catch(err) {
            console.log(err);
            return socket.emit('readerify', format("an error occurred :("));
        }
    });
});

app.get("/source", async (req, res) => {
    res.setHeader('Content-Type', 'application/javascript');
    res.send(fs.readFileSync(__filename));
});

/**
 * Helper function to try and retrieve the next section of a site if it exists.
 */
const loadNextPage = async (dom, socket) => {
    let targets = [
        ...Array.from(dom.window.document.querySelectorAll("a")), 
        ...Array.from(dom.window.document.querySelectorAll("button"))
    ];
    targets = targets.filter(e => (e.textContent + e.className).toLowerCase().includes("next"));

    if(targets.length == 0) return;
    let target = targets[targets.length - 1];
    
    if(target.tagName === "A") {
        let newDom = await refetch(socket, target.href);
        return newDom;
    }
    else if(target.tagName === "BUTTON") {
        dom.window.eval(target.getAttribute("onclick"));
        return dom;
    }

    return;
};    

/**
 * Helper function to return the readable HTML of a JSDOM object.
 */
const readerify = (dom) => {
    return (new Readability(dom.window.document.cloneNode(true))).parse();
};

/**
 * Helper function to validate URLs and fetch.
 */
const yoink = async (url) => {
    if(!url || typeof url !== "string" || !/^https?:\/\//.test(url)) {
        return {success: false, error: "invalid url!"};
    }
    try {
        let content = await (await fetch(url)).text();
        return {success: true, content};
    }
    catch(err) {
        return {success: false, error: "error fetching content!"};
    }
}

/**
 * Helper function to validate and load b64 string into a JSDOM object.
 */
const toDOM = (data) => {
    if(!data || typeof data !== "string") {
        return false;
    }
    return new JSDOM(data);
};

/**
 * Helper function to send another URL to a socket to render.
 */
const refetch = (socket, url) => {
    return new Promise(async (resolve, reject) => {
        socket.emit('fetch', await yoink(url));
        socket.bypass = true;
        socket.once('readerify', (data) => {
            resolve(toDOM(data));
        });
    });
};

server.listen(PORT, () => {
    console.log(`chall listening on 0.0.0.0:${PORT}`);
});
