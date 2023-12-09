const createError = require("http-errors");
const express = require("express");
const path = require("path");
const cookieParser = require("cookie-parser");
const logger = require("morgan");
const session = require("express-session");

const indexRouter = require("./routes/index");
const adminRouter = require("./routes/admin");
const authRouter = require("./routes/auth");
const accountRouter = require("./routes/account");
const apiRouter = require("./routes/api");

const app = express();

// view engine setup
app.set("views", path.join(__dirname, "views"));
app.set("view engine", "pug");

app.use(logger("dev"));
app.use(express.json());

app.use(cookieParser());
app.use(express.static(path.join(__dirname, "public")));
app.use(
    session({
        secret: process.env.SECRET_KEY,
        resave: false,
        saveUninitialized: false,
        cookie: {
            httpOnly: true,
            secure: app.get("env") === "production"
        },
    })
);


app.use("/", indexRouter);
app.use("/admin", adminRouter);
app.use("/auth", authRouter);
app.use("/account", accountRouter);
app.use("/api", apiRouter);

// catch 404 and forward to error handler
app.use((req, res, next) => {
    next(createError(404));
});

// error handler
app.use((err, req, res, next) => {
    // set locals, only providing error in development
    res.locals.message = err.message;
    res.locals.error = req.app.get("env") === "development" ? err : {};

    // render the error page
    res.status(err.status || 500);
    res.render("error", (logged = req.session && req.session.user));
});

module.exports = app;
