const express = require('express');
const {parseURL} = require('ufo');
const {createWriteStream, readFile, readFileSync, ensureDir, existsSync, unlink} = require('fs-extra');
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));
const apicache = require('apicache');
const rateLimit = require('express-rate-limit');
const path = require('path');
const https = require('https');

process.env.NODE_ENV = 'production';

const domains = ['try.harder'];
const bypassDomainCheck = false;
const port = 8080;
const dir = "app_files";

const app = express();
app.set('x-powered-by', false);
app.set('trust proxy', true);
app.set('etag', false);

const cache = apicache.middleware;
app.use(cache(10000));

const limiter = rateLimit({
  windowMs: 1 * 1000,
  max: 5,
  standardHeaders: false,
  legacyHeaders: false,
  message: "No scan needed"
})
app.use(limiter);

async function downloadFile(url,path){
  const res = await fetch(url);
  let fileStream = null;
  await new Promise((resolve, reject) => {
   if (res.status==200){
    fileStream = createWriteStream(path);
    res.body.pipe(fileStream);
    res.body.on("error", reject);
    fileStream.on("error", resolve);
    fileStream.on("finish", resolve);
   } else {
    reject(new Error('Nothing to fetch here..'));
   }
  });
};
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname+'/index.html'));
})


app.get('/*', async(req, res, next) => {
  const host = req.hostname;
  const protocol = req.protocol || 'http';
  const url = req.url;

  let [mod = '_', ...segments] = url.split('/');
  let id ="";
  let filePath="";
  
  try{
   id = decodeURIComponent(segments.join('/'));
   filePath = decodeURIComponent(req.path);
  }catch(error){
    res.status(500);
    res.send(`Bad URI`);
    return
  }

  const isLocal = !id.startsWith('http');

  if (isLocal) {
    id = `${protocol}://localhost${id.startsWith('/') ? '' : '/'}${id.startsWith('#') ? "" : id}`;
    filePath = filePath.startsWith('/#') ? "" : filePath;
  } else {
    const parsedUrl = parseURL(id, 'https://');
    
    if (!bypassDomainCheck) {
      let domainAllowed = false;

      if (domains.length > 0) {
        if (typeof domains === 'string') {
          domains = domains.split(',').map(s => s.trim());
        }

        const hosts = domains.map(domain => parseURL(domain, 'https://').host);

        if (hosts.includes(parsedUrl.host)) {
          domainAllowed = true;
          filePath = parsedUrl.host;
        }
      }

      if (!domainAllowed) {
        res.status(403);
        res.send(`Remote URL not on allowlist. Value(s) provided is/are: domain(s): ${JSON.stringify(domains)}`);
        return;
      }
    }
  } 

  try{
    await downloadFile(id,dir+filePath);
  }catch(error){
    res.status(403);
    res.send("Bad filePath");
    return;
  }

  readFile(dir+filePath,function(err, content){
    if(err){
      res.status(403);
      res.send(`Bad filePath`);
    }
    res.end(content);
    unlink(dir+filePath);
  })

});

const httpsServer = https.createServer({
  key: readFileSync('certif/privkey.pem'),
  cert: readFileSync('certif/fullchain.pem'),
}, app);

httpsServer.listen(443, () => {
    console.log('HTTPS Server running on port 443');
});

app.listen(port, () => {
  console.log(`⚡️[server]: Server is running at http://localhost:${port} `);
});

process.on('uncaughtException', err => {
  console.log(`Uncaught Exception: ${err.message}`);
  process.exit(1);
})