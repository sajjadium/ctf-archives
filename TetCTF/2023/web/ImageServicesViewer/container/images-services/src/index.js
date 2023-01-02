const express = require('express')
const morgan = require('morgan');
const path = require('path');
const bodyParser = require('body-parser')
const urlParse = require('url-parse');
const { URL, parse } = require('url');
const { spawnSync } = require('child_process');

const app = express()
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(morgan('common'));
app.set('views', path.join(__dirname, '/views'));
app.set('view engine', 'ejs')

//An error handling middleware
app.use(function (err, req, res, next) {
    console.error(err)
    return res.status(500).send("~.~ Something Went Wrong")
});

const isAdmin = (req, res, next) => {
    try {
        if (req.query.password.length > 12 || req.query.password != "Th!sIsS3xreT0") {
            return res.send("You don't have permission")
        }
        next();
    } catch (error) {
        return res.status(500).send("Oops, something went wrong.");
    }
}

const validate = (req, res, next) => {
    const allowedType = ["string", "number"];
    try {
        for (let key in req.body) {
            if (!allowedType.includes(typeof (req.body[key])) || isWAF(req.body[key]))
                return res.status(500).send("Oops, something went wrong.");
        }
        next();
    } catch (error) {
        return res.status(500).send("Oops, something went wrong.");
    }
}

app.get('/', function (req, res, next) {
    try {
        res.render('index')
    } catch (error) {
        next(error)
    }
})

app.post('/api/getImage', isAdmin, validate, async (req, res, next) => {
    try {
        const url = req.body.url.toString()
        let result = {}
        if (IsValidProtocol(url)) {
            const flag = isValidHost(url)
            if (flag) {
                console.log("[DEBUG]: " + url)
                let res = await downloadImage(url)
                result = res
            } else {
                result.status = false
                result.data = "Invalid host i.ibb.co"
            }

        } else {
            result.status = false
            result.data = "Invalid url"
        }
        res.json(result)
    } catch (error) {
        res.status(500).send(error.stack)
    }
})

const IsValidProtocol = (s, protocols = ['http', 'https']) => {
    try {
        new URL(s); ``
        const parsed = parse(s);
        return protocols
            ? parsed.protocol
                ? protocols.map(x => x.toLowerCase() + ":").includes(parsed.protocol)
                : false
            : true;
    } catch (err) {
        return false;
    }
};

const isValidHost = (url => {
    const parse = new urlParse(url)
    // console.log(parse)
    return parse.host === "i.ibb.co" ? true : false
})

const isWAF = (text) => {
    const blacklist = ["constructor", "render", "require", "include", "process", "child_process", "exec", "execSync", "spawn", "spawnSync", "global", "root", "mainModule", "arguments", "__proto__", "prototype", "\"", "'", "!", "[", "]", "|", "$", "&", "{", "}", "%0A", "%09", "(", ")", "`",","]
    for (let i of blacklist) {
        if (text.includes(i)) {
            return true
        }
    }
    return false
}

const downloadImage = async (url) => {
    try {
        let result = { status: false, data: "Invalid extension or content-type" }
        const cmd = spawnSync('python', ['bot.py', url]);
        const rawResponse = cmd.stdout.toString()
        if (rawResponse == 0) {
            return result
        } else {
            result.status = true
            result.data = rawResponse
            return result
        }
    } catch (error) {
        return result
    }
}

const port = 3000
app.listen(port, function () {
    console.log("[Start] Server starting:" + port)
})


