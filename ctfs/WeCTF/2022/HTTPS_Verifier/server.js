const express = require('express');
const https = require('https');
const axios = require('axios');
const dns = require('dns-sync');
const ipaddr = require('ipaddr.js');
const net = require('net');

const app = express();
app.set('view engine', 'ejs');

const logstashPort = 5044
const logstashHost = "localhost"


const log = (data) => {
    let client = new net.Socket();
    client.connect({ port: logstashPort, host: logstashHost })
    client.on('connect',function(){
        client.write(JSON.stringify({data}));
        client.end();
    });
}

const checkIp = (ip) => {
    if (!ipaddr.isValid(ip)) return false;
    try {
        const range = ipaddr.parse(ip).range();
        if (range !== 'unicast') return false; // Private IP Range
    } catch (err) {
        return false;
    }
    return true;
};

app.get('/', function (req, res) {
  res.render('index.ejs');
});

app.get('/query', async (req, res) => {
  const {host, port} = req.query;
  const integerPort = parseInt(port) || 443;
  if (!/^[a-z0-9|\.]+$/.test(host)) return res.send("hacker");
  try {
    if (!checkIp(dns.resolve(host))) return res.send("hacker");
    const httpsAgent = new https.Agent({rejectUnauthorized: false});
    await axios.get(`https://${host}:${integerPort}/`, {httpsAgent});
  } catch (e) {
    return res.send("not ok")
  }
  return res.send("ok")
})

app.listen(3000)
