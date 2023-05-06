import { createConnection } from "typeorm";
import * as express from "express";
import * as path from "path";
import * as http from "http";
import * as indexRouter from "./routes/index";
import * as secureRouter from "./routes/secure";
import * as fileUpload from "express-fileupload";
import * as cookieParser from "cookie-parser";

createConnection().then(() => {
    const app = express();
    const port = 3000;
    app.use(express.json());
    app.use(express.urlencoded({ extended: false }));
    app.use(express.static(path.join(__dirname, 'relier-front/build/')));
    app.use(cookieParser());
    app.use(fileUpload({
        useTempFiles : true,
        tempFileDir : '/tmp/',
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
