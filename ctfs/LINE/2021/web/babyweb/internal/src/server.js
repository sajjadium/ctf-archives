import { createSecureServer } from 'http2';
import { readFileSync } from 'fs';

import { router } from './router.js';

const onRequest = (req, res)=>{
  let r, path;
  if(req.httpVersion === "1.1"){ 
    path = req.url
    r = res
  } else { 
    path = req.headers[":path"]
    r = req.stream
  }
  router(req, r, path)
};

const server = createSecureServer({
  key: readFileSync('key.pem'),
  cert: readFileSync('cert.pem'),
  allowHTTP1: true,
}, onRequest);

server.on('error', (err) => console.error(err));

server.on('connect',()=>{
  console.log("Connected!")
});

server.listen(8443, ()=>{
  console.log("Server is running on port 8443!")
});

