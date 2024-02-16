const express = require('express');
const cookieParser = require('cookie-parser');
const path = require('path');
const bodyParser = require('body-parser');
const jwt = require('jsonwebtoken');


const app = express();
const PORT = 3000;

app.use(cookieParser());
app.use(bodyParser.urlencoded({ extended: true }));
app.set('views', path.join(__dirname, "view"));
app.set('view engine', 'ejs');

const mainToken = "Your_Token";
const mainuser="particular_username";

app.get('/', (req, res) => {
    let mainJwt = req.cookies.jwt || {};

    try {
        let jwtHead = mainJwt.split('.');

        let jwtHeader = jwtHead[0];
        jwtHeader = Buffer.from(jwtHeader, "base64").toString('utf8');
        jwtHeader = JSON.parse(jwtHeader);
        jwtHeader = JSON.stringify(jwtHeader, null, 4);
        mainJwt = {
            header: jwtHeader
        }

        let jwtBody = jwtHead[1];
        jwtBody = Buffer.from(jwtBody, "base64").toString('utf8');
        jwtBody = JSON.parse(jwtBody);
        jwtBody = JSON.stringify(jwtBody, null, 4);
        mainJwt.body = jwtBody;

        let jwtSignature = jwtHead[2];
        mainJwt.signature = jwtSignature;
    } catch(error) {
        if (typeof mainJwt === 'object') {
            mainJwt.error = error;
        } else {
            mainJwt = {
                error: error
            };
        }
    }
    res.render('index', mainJwt);
});

app.post('/updateName', (req, res) => {
    try {
        const newName = req.body.name;
        const token = req.cookies.jwt || ""; 
        const decodedToken = jwt.decode(token);
        decodedToken.name = newName;
        const newToken = jwt.sign(decodedToken, 'randomSecretKey');
        if (newName === mainuser) {
            res.cookie('jwt', mainToken);
        }else{
            res.cookie('jwt', newToken);
        }
        res.redirect('/');
    } catch (error) {
        res.redirect('/');
    }
});



app.listen(PORT, (err) => {
    console.log(`Server is Running on Port ${PORT}`);
});



                