// Inspiration: SekaiCTF scanner service

const express = require('express');
const { spawn } = require('child_process');
const shellQuote = require('shell-quote');
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
app.get('/checker', (req, res) => {
  let url = req.query.url;

  if (url) {

    let host;
    let port;

    // MakE it Safer!!!!! 
    if (url.includes(":")) {
      const parts = url.split(":");
      host = parts[0];
      port = parts.slice(1).join(":");
    } else {
      host = url;
    }
    if (port) {
      command = shellQuote.quote(["nmap", "-p", port, host]); // Construct the shell command
    } else {
      command = shellQuote.quote(["nmap", "-p", "80", host]);
    }
    nmap = spawn("bash", ["-c", command]);
    console.log(command);
    
    nmap.on('exit', function (code) {
      console.log('child process exited with code ' + code.toString());
      if (code !== 0) {
        res.send(`Error executing command!!!`);
      } else {
        res.send(`Ok...`);
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
