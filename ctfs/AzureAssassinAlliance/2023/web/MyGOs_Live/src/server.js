// Inspiration: SekaiCTF scanner service

const express = require('express');
const { spawn } = require('child_process');
const fs = require('fs');

const app = express();
const port = 3333;
app.use(express.static('public'));
app.get('/', (req, res) => {
  fs.readFile(__dirname + '/public/index.html', 'utf8', (err, data) => {
    if (err) {
      console.error(err);
      res.status(500).send('Internal Server Error');
    } else {
      // Send the HTML content
      res.send(data);
    }
  })
}
);
function escaped(c) {
  if (c == ' ')
    return '\\ ';
  if (c == '$')
    return '\\$';
  if (c == '`')
    return '\\`';
  if (c == '"')
    return '\\"';
  if (c == '\\')
    return '\\\\';
  if (c == '|')
    return '\\|';
  if (c == '&')
    return '\\&';
  if (c == ';')
    return '\\;';
  if (c == '<')
    return '\\<';
  if (c == '>')
    return '\\>';
  if (c == '(')
    return '\\(';
  if (c == ')')
    return '\\)';
  if (c == "'")
    return '\\\'';
  if (c == "\n")
    return '\\n';
  if (c == "*")
    return '\\*';
  else
    return c;
}
app.get('/checker', (req, res) => {
  let url = req.query.url;
  
  if (url) {
    if (url.length > 60) {
      res.send("我喜欢你");
      return;
    }
    url = [...url].map(escaped).join("");
    console.log(url);

    let host;
    let port;
    if (url.includes(":")) {
      const parts = url.split(":");
      host = parts[0];
      port = parts.slice(1).join(":");
    } else {
      host = url;
    }
    let command = "";
    // console.log(host);
    // console.log(port);

    if (port) {
      if (isNaN(parseInt(port))) {
        res.send("我喜欢你");
        return;
      }
      command = ["nmap", "-p", port, host].join(" "); // Construct the shell command
    } else {
      command = ["nmap", "-p", "80", host].join(" ");
    }

    var fdout = fs.openSync('stdout.log', 'a');
    var fderr = fs.openSync('stderr.log', 'a');
    nmap = spawn("bash", ["-c", command], {stdio: [0,fdout,fderr] } );

    nmap.on('exit', function (code) {
      console.log('child process exited with code ' + code.toString());
      if (code !== 0) {
        let data = fs.readFileSync('stderr.log');
        console.error(`Error executing command: ${data}`);
        res.send(`Error executing command!!! ${data}`);
      } else {
        let data = fs.readFileSync('stdout.log');
        console.error(`Ok: ${data}`);
        res.send(`${data}`);
      }
    });
  } else {
    res.send('No parameter provided.');
  }
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});

process.on('uncaughtException', (err) => {
  console.error('Uncaught Exception:', err);
});
