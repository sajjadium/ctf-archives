const express = require('express');
const cookieParser = require('cookie-parser');
const dotenv = require('dotenv');
dotenv.config();

const authRouter = express.Router();
authRouter.get('/auth', function(req, res, next) {
    return res.status(200).json(JSON.stringify({ token: process.env.TOKEN }));
});

authRouter.get('/a24', function(req, res, next) {
    return res.status(200).json(JSON.stringify({ token: process.env.TOKEN }));
});

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());

app.use('/', authRouter);

module.exports = app;
