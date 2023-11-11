const fs = require('fs');
const path = require('path');
const express = require('express');
const auth = require('express-basic-auth');
const mustache = require('mustache');
const app = express();

const SECRET = process.env["SECRET"] || "ADMIN_SECRET";
const FLAG = process.env["FLAG"] || "FakeCTF{panda-sensei}";
const BASIC_USERNAME = process.env["BASIC_USERNAME"] || "guest";
const BASIC_PASSWORD = process.env["BASIC_PASSWORD"] || "guest";

app.engine('html', function (filePath, options, callback) {
    fs.readFile(filePath, function (err, content) {
        if (err) return callback(err);
        let rendered = mustache.render(content.toString(), options);
        return callback(null, rendered);
    });
});
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'html');
app.use(express.json());
app.use(auth({
    challenge: true,
    unauthorizedResponse: () => {
        return "Unauthorized";
    },
    authorizer: (username, password) => {
        return auth.safeCompare(username, BASIC_USERNAME)
            && auth.safeCompare(password, BASIC_PASSWORD);
    }
}));

const isAdmin = req => req.query.secret === SECRET;
const getAdminRole = req => {
    /* Return array of admin roles (such as admin, developer).
       More roles are to be added in the future. */
    return isAdmin(req) ? ['admin'] : [];
}
let memo = {};

app.get('/', (req, res) => res.render('index'));

/** Create new memo */
app.post('/new', (req, res) => {
    /* Create new memo */
    if (!(req.ip in memo)) memo[req.ip] = [];
    memo[req.ip].push("");

    res.json({status: 'success'});
});

/** Delete memo */
app.post('/del', (req, res) => {
    let index = req.body.index;

    /* Delete memo */
    if ((req.ip in memo) && (index in memo[req.ip])) {
        memo[req.ip].splice(index, 1);
        res.json({status: 'success', result: 'Successfully deleted'});
    } else {
        res.json({status: 'error', result: 'Memo not found'});
    }
});

/** Get memo list */
app.get('/show', (req, res) => {
    let ip = req.ip;

    /* We don't need to call isAdmin here
       because only admin can see console log. */
    if (req.body.debug == true)
        console.table(memo, req.body.inspect);

    /* Admin can read anyone's memo for censorship */
    if (getAdminRole(req)[0] !== undefined)
        ip = req.body.ip;

    /* Return memo */
    if (ip in memo)
        res.json({status: 'success', result: memo[ip]});
    else
        res.json({status: 'error', result: 'Memo not found'});
});

/** Edit memo */
app.post('/edit', (req, res) => {
    let ip = req.ip;
    let index = req.body.index;
    let new_memo = req.body.memo;

    /* Admin can edit anyone's memo for censorship */
    if (getAdminRole(req)[0] !== undefined)
        ip = req.body.ip;

    /* Update memo */
    if (ip in memo) {
        memo[ip][index] = new_memo;
        res.json({status: 'success', result: 'Successfully updated'});
    } else {
        res.json({status: 'error', result: 'Memo not found'});
    }
});

/** Admin panel */
app.get('/admin', (req, res) => {
    res.render('admin', {is_admin:isAdmin(req), flag:FLAG});
});

app.listen(3000, () => {
    console.log("Server is up!");
});
