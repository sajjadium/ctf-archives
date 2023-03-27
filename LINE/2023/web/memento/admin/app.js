const createError = require("http-errors");
const express = require("express");
const logger = require("morgan");
const { chromium } = require('playwright');
const app = express();
const PORT = process.env.PORT || 10000;
const FLAG = process.env.FLAG || "LINECTF{redacted}";

app.use(logger("common"));

const router = express.Router();

const asyncWrapper = (fn) => {
    return (req, res, next) => {
        return fn(req, res, next).catch(next);
    };
};

router.get(
    "/",
    asyncWrapper(async function (req, res, next) {
        const url = req.query.url;
        origin = `http://${req.connection.remoteAddress.match(
            /(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/
        )}:${PORT}`;
        console.log(url);
        if (url && url.startsWith("/")) {
            const browser = await chromium.launch({
                headless: true
            });
            const context = await browser.newContext();
            const page = await context.newPage();

            // post flag as anonymous user
            console.log(origin + "/bin/create");
            await page.goto(origin + "/bin/create");
            await page.type("textarea", FLAG);
            await page.click("button");

            // visit to reported url
            await page.goto(origin + url);

            await context.close();
            await browser.close();
        }
        res.header("Access-Control-Allow-Origin", "*");
        res.send("ok");
    })
);

router.get("/status", (req, res, next) => {
    res.send("running");
});

app.use(router);

// catch 404 and forward to error handler
app.use(function (req, res, next) {
    next(createError(404));
});

// error handler
app.use(function (err, req, res, next) {
    console.log(err);
    res.status(err.status || 500);
    res.send("error");
});

module.exports = app;
