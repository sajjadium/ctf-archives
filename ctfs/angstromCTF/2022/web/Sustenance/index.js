const express = require("express");
const cookieParser = require("cookie-parser");
const path = require("path");

const app = express();
app.use(express.urlencoded({ extended: false }));

// environment config
const port = Number(process.env.PORT) || 8080;
const adminSecret = process.env.ADMIN_SECRET || "secretpw";
const flag =
    process.env.FLAG ||
    "actf{someone_is_going_to_submit_this_out_of_desperation}";

function queryMiddleware(req, res, next) {
    res.locals.search =
        req.cookies.search || "the quick brown fox jumps over the lazy dog";
    // admin is a cool kid
    if (req.cookies.admin === adminSecret) {
        res.locals.search = flag;
    }
    next();
}

app.use(cookieParser());

app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "index.html"));
});

app.post("/s", (req, res) => {
    if (req.body.search) {
        for (const [name, val] of Object.entries(req.body)) {
            res.cookie(name, val, { httpOnly: true });
        }
    }
    res.redirect("/");
});

app.get("/q", queryMiddleware, (req, res) => {
    const query = req.query.q || "h"; // h
    let status;
    if (res.locals.search.includes(query)) {
        status =
            "succeeded, but please give me sustenance if you want to be able to see your search results because I desperately require sustenance";
    } else {
        status = "failed";
    }
    res.redirect(
        "/?m=" +
            encodeURIComponent(
                `your search that took place at ${Date.now()} has ${status}`
            )
    );
});

app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
});
