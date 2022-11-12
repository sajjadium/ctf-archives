const flash = (req, res, type, msg, url) => {
    let endpoint = url || req.originalUrl;
    let delim = endpoint.includes("?") ? "&" : "?";
    return res.redirect(`${endpoint}${delim}${type}=${encodeURIComponent(msg)}`);
};

const isLocalhost = req => ((req.ip == '127.0.0.1') ? 0 : 1);

module.exports = { flash, isLocalhost };