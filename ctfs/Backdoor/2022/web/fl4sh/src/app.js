"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const typeorm_1 = require("typeorm");
const express = require("express");
const path = require("path");
const http = require("http");
const indexRouter = require("./routes/index");
const secureRouter = require("./routes/secure");
const fileUpload = require("express-fileupload");
const cookieParser = require("cookie-parser");
typeorm_1.createConnection().then(() => {
    const app = express();
    const port = 3000;
    app.use(express.json());
    app.use(express.urlencoded({ extended: false }));
    app.use(express.static(path.join(__dirname, 'relier-front/build/')));
    app.use(cookieParser());
    app.use(fileUpload({
        useTempFiles: true,
        tempFileDir: '/tmp/',
        limits: { fileSize: 50 * 1024 * 1024 },
    }));
    app.use('/api', indexRouter);
    app.use('/api/secure', secureRouter);
    app.set('port', port);
    app.get('/cdn/:secret', function (req, res) {
        res.sendFile(path.join(__dirname, 'images/', req.params.secret));
    });
    app.get('/:any', function (req, res) {
        res.sendFile(path.join(__dirname, 'relier-front/build', 'index.html'));
    });
    app.get('/home/:teamSecret', function (req, res) {
        res.sendFile(path.join(__dirname, 'relier-front/build', 'index.html'));
    });
    app.get('/vc/:sid', function (req, res) {
        res.sendFile(path.join(__dirname, 'relier-front/build', 'index.html'));
    });
    app.get('/team/:secret', function (req, res) {
        res.sendFile(path.join(__dirname, 'relier-front/build', 'index.html'));
    });
    const server = http.createServer(app);
    server.listen(port);
});
