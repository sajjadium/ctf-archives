const express = require('express')
const path = require('path');
const bodyParser = require('body-parser')
const fetch = (...args) => import('node-fetch').then(({ default: fetch }) => fetch(...args));

const app = express()
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
    extended: true
}));
app.use("/", express.static(__dirname + "/static"));
app.set('views', path.join(__dirname, '/views'));


const isObject = obj => obj && obj.constructor && obj.constructor === Object;
const merge = (dest, src) => {
    for (var attr in src) {
        if (isObject(dest[attr]) && isObject(src[attr])) {
            merge(dest[attr], src[attr]);
        } else {
            dest[attr] = src[attr];
        }
    }
    return dest
};

app.get('/', function (req, res, next) {
    try {
        res.send('index.html')
    } catch (error) {
        res.send(error)
    }
})

app.post('/api/tet/years', function (req, res, next) {
    try {
        const list = req.body.list.toString();
        const getList = require("./static/" + list)
        res.json(getList.all())
    } catch (error) {
        res.send(error)
    }
})

app.post('/api/tet/list', function (req, res, next) {
    try {
        const getList1 = require("./static/list-2010-2016.js")
        const getList2 = require("./static/list-2017-2022.js")
        let newList = merge(getList1.all(), getList2.all())
        let data = req.body.data || "";
        newList = merge(newList, data);
        res.json(newList)
    } catch (error) {
        res.send(error)
    }
})

app.get('/api/tet/countdown', async function (req, res, next) {
    try {
        const response = await fetch('http://countdown:8084/tet/countdown');
        const data = await response.text();
        res.send(data)
    } catch (error) {
        res.send(error)
    }
})

const port = 3000
app.listen(port, function () {
    console.log("[Start] Server starting:" + port)
})


