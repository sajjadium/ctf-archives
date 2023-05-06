const express = require("express");
const app = express();
const Database = require("./src/db.js");
const util = require("./src/util.js");

const PORT = process.env.PORT || 9000;
global.db = new Database('baby_client.db');

app.set("view engine", "ejs");
app.use(express.urlencoded({ extended: false }));
app.use(express.static("public"));

app.use((req, res, next) => {
    res.setHeader("Content-Security-Policy", `
        default-src 'self';
        style-src 'self' https://fonts.googleapis.com;
        font-src https://fonts.gstatic.com;
        object-src 'none';
        base-uri 'none';
        frame-ancestors 'none';
    `.trim().replace(/\s+/g, " "));
    res.setHeader("X-Frame-Options", "DENY");
    next();
});

app.use("/search", require("./routes/search.js"));
app.use("/scan", require("./routes/scan.js"));

app.get("/", (req, res) => res.render("index"));

(async () => {
    await db.connect();
    await db.migrate();

    app.listen(PORT, '0.0.0.0', () => console.log(`Listening on port ${PORT}`));
})();