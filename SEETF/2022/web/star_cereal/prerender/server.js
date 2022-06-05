'use strict';

const { match } = require('assert');
const prerender = require('prerender');
const prMemoryCache = require('prerender-memory-cache');
const url = require('url');

const server = prerender({
    chromeFlags: ['--no-sandbox', '--headless', '--disable-gpu', '--remote-debugging-port=9222', '--hide-scrollbars', '--disable-dev-shm-usage'],
    forwardHeaders: true,
    chromeLocation: '/usr/bin/chromium-browser'
});

const memCache = Number(process.env.MEMORY_CACHE) || 0;
if (memCache === 1) {
    server.use(prMemoryCache);
}

server.use(prerender.blacklist());
server.use(prerender.httpHeaders());

// Hacker, you are?
// Get flag, you do not.

const validateUrls = (req, res, next) => {

    let matches = url.parse(req.prerender.url).href.match(/^(http:\/\/|https:\/\/)app/gi)
    if (!matches) {
        return res.send(403, 'NO_FLAG_FOR_YOU_MUAHAHAHA');
    }
    
    next();
}

// Adapted from https://github.com/prerender/prerender/blob/master/lib/plugins/removeScriptTags.js
// except return a 403 instead of replacing the script tag
const noScriptsPlease = (req, res, next) => {
    
    if (!req.prerender.content || req.prerender.renderType != 'html') {
        return next();
    }

    var matches = req.prerender.content.toString().match(/<script(?:.*?)>(?:[\S\s]*?)<\/script>/gi);
    if (matches)
        return res.send(403, 'NO_FLAG_FOR_YOU_MUAHAHAHA');

    matches = req.prerender.content.toString().match(/<link[^>]+?rel="import"[^>]*?>/i);
    if (matches)
        return res.send(403, 'NO_FLAG_FOR_YOU_MUAHAHAHA');

    next();
}

server.use({
    requestReceived: validateUrls,
    pageLoaded: noScriptsPlease
});

server.start();