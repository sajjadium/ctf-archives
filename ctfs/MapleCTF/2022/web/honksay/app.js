const express = require("express");
const cookieParser = require('cookie-parser');
const goose = require("./goose");
const clean = require('xss');

const app = express();
app.use(cookieParser());
app.use(express.urlencoded({extended:false}));

const PORT = process.env.PORT || 9988;

const headers = (req, res, next) => {
    res.setHeader('X-Frame-Options', 'DENY');
    res.setHeader('X-Content-Type-Options', 'nosniff');
    return next();
  }
app.use(headers);
app.use(express.static('public'))

const template = (goosemsg, goosecount) => `
<html>
<head>
<style>
H1 { text-align: center }
.center {
    display: block;
    margin-left: auto;
    margin-right: auto;
    width: 50%;
  }

  body {
    place-content:center;
    background:#111;
  }

  * {
    color:white;
  }

</style>
</head>
${goosemsg === '' ? '': `<h1> ${goosemsg} </h1>`}
<img src='/images/goosevie.png' width='400' height='700' class='center'></img>
${goosecount === '' ? '': `<h1> You have honked ${goosecount} times today </h1>`}

<form action="/report" method=POST style="text-align: center;">
  <label for="url">Did the goose say something bad? Give us feedback.</label>
  <br>
  <input type="text" id="site" name="url" style-"height:300"><br><br>
  <input type="submit" value="Submit" style="color:black">
</form>
</html>
`;


app.get('/', (req, res) => {
    if (req.cookies.honk){
        //construct object
        let finalhonk = {};
        if (typeof(req.cookies.honk) === 'object'){
            finalhonk = req.cookies.honk
        } else {
            finalhonk = {
                message: clean(req.cookies.honk), 
                amountoftimeshonked: req.cookies.honkcount.toString()
            };
        }
        res.send(template(finalhonk.message, finalhonk.amountoftimeshonked));
    } else {
        const initialhonk = 'HONK';
        res.cookie('honk', initialhonk, {
            httpOnly: true
        });
        res.cookie('honkcount', 0, {
            httpOnly: true
        });
        res.redirect('/');
    }
});

app.get('/changehonk', (req, res) => {
    res.cookie('honk', req.query.newhonk, {
        httpOnly: true
    });
    res.cookie('honkcount', 0, {
        httpOnly: true
    });
    res.redirect('/');
});

app.post('/report', (req, res) => {
    const url = req.body.url;
    goose.visit(url);
    res.send('honk');
});

app.listen(PORT, () => console.log((new Date())+`: Web/honksay server listening on port ${PORT}`));
