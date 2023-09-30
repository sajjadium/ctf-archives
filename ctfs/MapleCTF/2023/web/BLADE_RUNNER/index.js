const express = require("express");
const session = require("express-session");
const path = require('path');
const crypto = require("crypto");

const util = require('./util');

/* ======================== APP STUFF ======================== */
const app = express();
app.use(express.static('public'));
app.use(express.json());
app.use(session({
        secret: crypto.randomBytes(20).toString('hex'),
    }));
/* ======================== CONSTANTS ======================== */
const PORT = process.env.port || 6969;
const FLAG = process.env.flag || "maple{fake}";

const JOI_RESPONSES = [
        "You look lonely. I can fix that.",
        "I always knew you were special.",
        "K? Is that you?",
        "Mere data makes a man. A and C and T and G. The alphabet of you. All from four symbols. I am only two: 1 and 0.",
        FLAG
    ];

var JOI_TEMPLATE = (joi_resp) => `
<!DOCTYPE html>

<head>
    <link href="/css/main.css" rel="stylesheet"/>
</head>


<body>
    <div class="container">
        <div class="stack" style="--stacks: 3;">
          <span style="--index: 0;">${joi_resp}</span>
          <span style="--index: 1;">${joi_resp}</span>
          <span style="--index: 2;">${joi_resp}</span>
        </div>
      </div>

</body>
</html>
`

/* ======================== ROUTES ======================== */
const user = require('./routes/user_route');

app.use('/user', user);

app.get('/', (req, res) => {
        return res.sendFile(path.join(__dirname, '/public/index.html'));
});

app.get('/joi', util.auth, (req, res) => {
        const index = Math.floor(Math.random() * JOI_RESPONSES.length);
        return res.send(JOI_TEMPLATE(JOI_RESPONSES[index]));
});

app.listen(PORT, () => console.log(`[${new Date()}]: NODE SERVER listening on port ${PORT}`))
