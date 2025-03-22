const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const app = express();
const cookieParser = require('cookie-parser');
app.use(cookieParser());
app.use(express.json())
app.set('view engine', 'ejs');
const port = process.env.PORT || 3000

app.use(express.static(__dirname + '/public'));

app.use(cors())

const users = [
    { name: 'user', password: 'pwd' },
    { name: 'admin', password: Math.random().toString(32), isAdmin: true },
];

const myLoaction = [
    { flag: "GLUG{f4k3_fl4g_f0r_t3st1ng}" }
]

function findUser(auth) {
    return users.find((u) =>
        u.name === auth.name &&
        u.password === auth.password);
}

app.use(bodyParser.json());


app.get('/', (req, res) => {

    historys = [];
    const data = historys

    res.render('index', { data });
});

app.post('/', (req, res) => {
    console.log(req.body)
    const user = findUser(req.body.auth || {});

    if (!user) {
        res.status(403).send({ ok: false, error: 'Access denied' });
        return;
    }

    const history = {
        icon: '👋',
    };

    Object.assign(history,req.body.location)

    if (history.isAdmin == true) {
        res.status(200).send(myLoaction)

    } else {
        res.status(200).send(history)
    }
})

app.listen(port);
console.log(`Listening on port ${port}`);