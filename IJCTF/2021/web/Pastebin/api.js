const { v4: uuidv4 } = require('uuid');
uuidv4();
var db = new Map()

function createPaste(req, res) {
  var {content} = req.body;
  noteid = uuidv4()
  db.set(noteid,{body:content})
  res.redirect(301,`/paste.html?id=${noteid}`)
}

function getPaste(req, res) {
  return res.json(db.get(req.params.id))
}


module.exports = {getPaste,createPaste}
