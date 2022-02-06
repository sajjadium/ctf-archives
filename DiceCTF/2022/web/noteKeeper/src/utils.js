const jwt = require("./jwt.js");

const jsonp = (req, res, type, data) => {
    if(req.query.callback && (typeof req.query.callback !== "string" || req.query.callback.includes('eval'))) {
        return res.status(400).send('no');
    }
    req.query.callback = req.query.callback || "load_" + type;
    res.jsonp(data);
};

const alert = (req, res, type, msg) => {
    jwt.signData(res, req.user?.username, { type, msg });
};

module.exports = { jsonp, alert };