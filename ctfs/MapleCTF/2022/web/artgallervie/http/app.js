const express = require('express');
const app = express();
const redis = require("redis");
const session = require('express-session');
const crypto = require('crypto');
const fileUpload = require('express-fileupload');
const serialize = require('node-serialize');
const cp = require("child_process");

app.use(fileUpload());

app.set('view engine', 'ejs');
app.use(express.urlencoded({ extended: false }));
app.use('/files', express.static('../ftp/files'));

const PORT = process.env.port || 8080;
const SECRET = crypto.randomBytes(20).toString('hex');

/*================================ REDIS ================================*/

let redisClient = redis.createClient();

redisClient.on('error', (err) => console.log('Redis Client Error', err));

redisClient.connect().then(() => {
    console.log("[Redis cli] Succesfully connected to Redis server.");
});

redisClient.on("error", function (err) {
    console.log("Error " + err);
});

/*=======================================================================*/


/*============================== SESSIONS ===============================*/

app.use(session({
    secret: SECRET,
    resave: false,
    saveUninitialized: false,
    cookie: {
        name: 'test',
        secure: false,
        httpOnly: false,
        maxAge: 1000 * 60 * 10
    }
}));

/*=======================================================================*/

app.use(async function (req, res, next) {
    if (req.session.art_token) {
        let val = await redisClient.get(`image_${req.session.art_token}`);
        let data_arr = serialize.unserialize(await redisClient.get(`image_${req.session.art_token}`));
        console.log(data_arr);
        req.images = []
        for (let key in data_arr) {
            req.images.push(data_arr[key]);
        }
    }
    res.on("finish", async function () {
        console.log(req.session);
        if (req.session){
            if (req.session.art_token) {
                await redisClient.set(`image_${req.session.art_token}`, serialize.serialize(req.images));
                let data = await redisClient.get(`image_${req.session.art_token}`);
            }
        }
    });
    next();
});


app.get("/", (req, res) => {
    if (req.session.key && req.session.art_token) {
        res.render('pages/gallery', {
            user: req.session.key,
            images: req.images,
            token: req.session.art_token
        });
    } else {
        res.render('pages/index');
    }
});

app.post("/login", (req, res) => {
    //idk someone told me i should make tokens out of my art or something??
    req.session.art_token = crypto.randomBytes(10).toString('hex');
    req.session.key = req.body.name;
    //default photos (drawn by Vie)
    req.images = ['goose.png', 'girl.png', 'bunny.png', 'motorcycle.png'];
    res.redirect("/");
});

app.get("/upload", (req, res) => {
    if (req.session.art_token) {
        res.render('pages/upload');
    } else {
        res.redirect('/');
    }

});

app.post("/upload", (req, res) => {
    if (req.session.art_token) {
        //People can upload max 4 images, which are inserted into their images array rolling basis
        let random_filename = crypto.randomBytes(10).toString('hex') + ".png";

        //high quality design 
        req.files.file.mv(`/usr/src/app/ftp/files/${random_filename}`);

        req.images.push(random_filename);
        req.images.shift();
        res.redirect("/");
    } else {
        res.redirect("/");
    }
});

app.get('/logout', function (req, res) {
    if(req.session) {
        req.session.destroy(function (err) {
            if (err) {
                console.log(err);
                res.send('Err :/');
            } else {
                res.redirect('/');
            }
        });
    } else {
        res.redirect('/');
    }

});


app.get('/query', async (req, res) => {
    let host = req.query.host;
    const port = parseInt(req.query.port);
    try {
        //im aware its bad 
        cp.execFileSync("curl", ['-k', '-L', `https://${host}:${port}/`]);
    } catch (e) {
        console.log("Error encountered");
        console.log(e);
    }
    res.send("The curator will observe your art");
});



app.use(function (req, res, next) {
    next();
});


app.listen(PORT, () => console.log((new Date()) + `:Node server listening on port ${PORT}`));
