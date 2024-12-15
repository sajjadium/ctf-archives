const express = require('express');
const bodyParser = require('body-parser');
const cp = require('child_process');
const app = express();
const port = 1337;

app.use(bodyParser.json());


app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});


function checkIP(ip) {
    if (typeof ip !== 'string') 
        return false;
    if (ip.indexOf('.') == -1)
        return false;
    let parts = ip.split('.');
    if (parts.length !== 4) 
        return false;
    for (let part of parts) {
        let num = parseInt(part);
        if (isNaN(num) || num < 0 || num > 255)
            return false;
    }
    return true;
}

app.post('/ping', (req, res) => {
    let ip = req.body.ip;
    if (!checkIP(ip))
        return res.json({result: 'Invalid IP address'});
    cmd = `ping -c 1 ${ip}`;
    cp.exec(cmd, (err, stdout, stderr) => {
        if (err) {
            return res.json({result: 'Error: ' + err.message});
        }
        if (stderr) {
            return res.json({result: 'Error: ' + stderr});
        }
        return res.json({result: stdout});
    });
});

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});