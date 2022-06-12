const express = require('express');
const cookieParser = require('cookie-parser')
const { randomBytes } = require('crypto');
const crypto = require('crypto');
const multer  = require('multer');
const os = require("os")
const SALT = "WECTF"

// keeps the mapping between user and files
FILE_DB = {};
// keeps the mapping between token and user data
USER_DB = {};

const app = express();
const upload = multer({ dest: os.tmpdir(), limits: {fileSize: 1024 * 1024} })
app.set('view engine', 'ejs');
app.use(cookieParser())
app.use(express.static('public'));

// return sha256(content)
function hashing(content){
  return crypto.createHash('sha256').update(SALT + content + SALT).digest('hex');
}

function get_token_from_req(req){
  let token = req.headers.token;
  if (!token) return null;
  return hashing(token)
}

function get_token_from_cookie(req){
  let token = req.cookies.token;
  if (!token) return {hashedToken: null, token: null};
  return {hashedToken: hashing(token), token}
}

// let user download file only once & csp for security
app.use(function (req, res, next) {
  res.set("Content-Security-Policy", `frame-ancestors 'none'; object-src 'none'; style-src 'self' https://fonts.googleapis.com; font-src https://fonts.gstatic.com/; script-src 'unsafe-inline';`)
  if (req.url.includes("/files/"))
    res.set('Cache-control', 'max-age=1000000')
  next();
});

// redirect to registration
const registerToken = (req, res) => res.redirect(`/register_token?back=${req.url}`)
const templatesRetrieveToken = (req, res) => {
  let {hashedToken, token} = get_token_from_cookie(req);
  if (!token) {
    registerToken(req, res)
    return
  }
  if (!USER_DB.hasOwnProperty(hashedToken)) {
    registerToken(req, res)
    return
  }
  return {hashedToken, token}
}

// render templates
app.get("/", (req, res) => {
  const tokenInfo = templatesRetrieveToken(req, res);
  if (!tokenInfo) return
  res.render("index", {token: tokenInfo.token, lastFile: USER_DB[tokenInfo.hashedToken][0] || ""})
})

app.get("/download/:token", (req, res) => {
  if (!templatesRetrieveToken(req, res)) return
  res.render("download", {file_token: req.params.token})
})

app.get("/sync_token", (req, res) => {
  res.render(`sync_token`)
})

// authentication stuffs
app.get("/register_token", (req, res) => {
  const {back} = req.query;
  if (!back) return res.send("wtf")
  // generate a token for user
  const token = randomBytes(32).toString("hex");
  USER_DB[hashing(token)] = [];
  res.cookie("token", token)
  // redirect to /sync_token which redirects back to ${back}
  res.redirect(`/sync_token?token=${token}&back=${encodeURI(back)}`)
})

// main logic
// upload file
app.post("/upload/:receiver", upload.single('file'), (req, res) => {
  let token = get_token_from_req(req);
  if (!token) return res.send("no token set")
  if (!USER_DB.hasOwnProperty(token)) return res.send("not a registered token")
  const receiver = req.params.receiver;
  let file_token = randomBytes(32).toString("hex");
  FILE_DB[hashing(file_token)] = {
    name: req.file.originalname, location: req.file.path, receiver: hashing(receiver), sender: token, logs: []}
  USER_DB[token].push(file_token)
  res.send({success: true, file_token});
})

// get info of file with token
app.get("/file_info/:token", (req, res) => {
  const hashed_file_token = hashing(req.params.token);
  if (!FILE_DB.hasOwnProperty(hashed_file_token)) return res.send({success: false, message: "no such file"})
  // log things!
  FILE_DB[hashed_file_token].logs.push({
    ip: req.headers['x-forwarded-for'] || req.socket.remoteAddress,
    source: req.headers.referer || req.url,
    time: Date.now()
  })
  let token = get_token_from_req(req);
  if (!token) return res.send({success: false, message: "no token set"})
  // needs the token to match either sender or receiver
  if (token === FILE_DB[hashed_file_token].sender || token === FILE_DB[hashed_file_token].receiver){
    const file_obj = FILE_DB[hashed_file_token]
    return res.send({
      success: true,
      result: {name: file_obj.name, path: file_obj.location, logs: file_obj.logs}
    })
  }
  res.send({success: false, message: "not your file"})
})

// download file
app.get("/files/:token", (req, res) => {
  let token = get_token_from_req(req);
  if (!token) return res.send({success: false, message: "no token set"})
  const hashed_file_token = hashing(req.params.token);
  if (!FILE_DB.hasOwnProperty(hashed_file_token))
    return res.send({success: false, message: "no such file"})
  if (token === FILE_DB[hashed_file_token].sender || token === FILE_DB[hashed_file_token].receiver)
    return res.sendFile(FILE_DB[hashed_file_token].location)
  res.send("not your file")
})


app.listen(80, () => {console.log(`started`)})
