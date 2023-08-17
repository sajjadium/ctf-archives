const path = require('path');
const express = require('express');
const cors = require('cors');
const { css, manifest, favicon, scripts } = require('./viewUtil');
const { name, version } = require('../package.json');
const PORT = process.env.PORT || 3000;
const app = express();
app.use(cors());

app.set('view engine', 'ejs');

app.get(`/health`, (req, res) =>
    res.status(200).json({ name, version, status: 'up' })
);

let apiHost;

if (process.env.REACT_APP_API_ROOT) {
    console.log(`REACT_APP_API_ROOT: ${process.env.REACT_APP_API_ROOT}`);
    apiHost = process.env.REACT_APP_API_ROOT;
} else {
    console.log(
        'No api host set, please use env variable REACT_APP_API_ROOT to set host'
    );
}

if (process.env.REACT_APP_ROOT) {
    console.log(`REACT_APP_ROOT: ${process.env.REACT_APP_ROOT}`);
    appHost = process.env.REACT_APP_ROOT;
} else {
    console.log(
        'No app host set, please use env variable REACT_APP_ROOT to set host'
    );
}

app.get(['/', '/note/*', '/new/*', '/newTicket/*'], function(req, res) {
    res.render('index', {
        config: { REACT_APP_API_ROOT: apiHost, REACT_APP_ROOT: appHost },
        css,
        manifest,
        favicon,
        scripts
    });
});

app.use(express.static(path.join(__dirname, '../build')));

app.listen(PORT, () =>
    console.log(`server running on on http://localhost:${PORT}}`)
);
