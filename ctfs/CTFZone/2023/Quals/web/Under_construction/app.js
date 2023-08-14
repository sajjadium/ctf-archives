const http = require('http');
const static = require('node-static');
const url_lib = require('url');
const puppeteer = require('puppeteer');
const { Worker } = require('worker_threads')

const hostname = '0.0.0.0';
const port = 3000;
var file = new static.Server('./app');


function verifyUrl(data) {
  if (!("url" in data))
    return false
  let url = data["url"].toString().trim();
  if (typeof url !== 'string' || (!url.startsWith('http://') && !url.startsWith('https://'))) {
    return false;
  }
  return url
}

const server = http.createServer((req, res) => {
  
  const url = req.url;
  const method = req.method;

  if(url.startsWith("/browser") && method === "GET")
  {
    let query = url_lib.parse(req.url,true).query;
    let site_url = verifyUrl(query);
    if (site_url === false)
    {
      res.statusCode = 400;
      res.setHeader('Content-Type', 'text/plain');
      res.end("Invalid url");
    }
    else
    {
      console.log('Visiting', site_url);
      try {
        const worker = new Worker('./worker.js',{workerData: site_url});
        worker.onerror = (event) => {
          console.log(event);
        };
        res.statusCode = 200;
        res.setHeader('Content-Type', 'text/plain');
        res.end(site_url);

      } catch (error) {
        console.error(error);
        res.statusCode = 400;
        res.setHeader('Content-Type', 'text/plain');
        res.end('Error');
      }

    }
  } 
  else
  {
    req.addListener('end', function () {
      file.serve(req, res);
    }).resume();
  }
  
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
