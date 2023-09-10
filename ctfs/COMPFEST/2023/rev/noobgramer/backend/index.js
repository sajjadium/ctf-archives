const express = require('express');
const router = express.Router();
const app = express();
const jws = require('jws');
const cors = require('cors');
const JWT_SECRET_KEY = "REDACTED";
const SECRET = "REDACTED";
const MESSAGE = "REDACTED";
const ADMIN= {password : "REDACTED", username:"REDACTED"};

const PORT = 8080;

let admin_notes = [
"REDACTED",
"REDACTED"
]

let guest_notes = [

]


function getJWTToken(req) {
  if (req.get("X-JWT-TOKEN")) {
   return req.get("X-JWT-TOKEN");
  }
  return null;
}

function getAuthorizationToken(req){
  if (req.headers.authorization) {
    return req.headers.authorization;
   }
   return null;
}

function requestProfile(req, str2) {
  const str1 = getAuthorizationToken(req)
  if (!str1){
    return "";
  }
  if (str1 === str2){
    return str1
  }
    let sum = 0;
    for (let i = 0; i < str2.length; i++) {
      sum += str2.charCodeAt(i);
    }
    return str1 - sum;
}

function middleware(req, res, next) {

  let token = getJWTToken(req);
  let payload = jws.decode(token, {complete: true});
  let header = payload.header;
  let valid;
  try {
    valid = jws.verify(token, header.alg, JWT_SECRET_KEY);
  } catch (e) {
    return next(e);
  }
  if (!valid) return next('invalid jwt');

  req.user = payload.payload;
  return next();
}

app.use(express.json());
app.use(cors(
  {origin: "*"}
))
app.get('/api/admin_only/:id', middleware, function(req, res, next) {
  
  if (requestProfile(req, SECRET) != SECRET) return res.sendStatus(403);
  
  if (!req.user.isAdmin && req.user.grantedAuthority !== "ALL") return res.sendStatus(403);
  const id = req.params.id;
  if (!admin_note[id]){
    res.status(404).send({message : "not found"})
  }
  const note = admin_note[id]
  res.status(200).json({note: note});
});


app.get('/api/priv/:id', function(req, res) {

  if (requestProfile(req, MESSAGE) != SECRET) return res.sendStatus(403);

  const id = parseInt(req.params.id);
  console.log(guest_notes[id])
  if (!guest_notes[id]){
    res.status(404).json({message : "not found"})
  }
  const note = guest_notes[id];
  guest_notes.splice(id, 1);
  res.status(200).json({note: note});
});

app.use(express.json());
app.use(cors(
  {origin: "*"}
))
app.post('/api/priv', function(req, res) {

  console.log(req.headers.authorization, requestProfile(req, MESSAGE), SECRET)
  if (requestProfile(req, MESSAGE) != SECRET) return res.sendStatus(403);

  const note = req.body.note;
  guest_notes.push(note);
  admin_notes.push(note);

  res.status(200).json({id : guest_notes.length - 1});
});



app.get('/', function(req, res, next) {
  res.send({status:'ok', msg: 'Hello World'});
})

app.listen(PORT, function() {
  console.log(`Server is listening on port ${PORT}...`);
});