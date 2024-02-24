const express = require('express');
const fs = require('fs');
const protobuf = require('protobufjs');
const glob = require('glob');
const { healthCheck } = require('./bot');
const app = express();
const port = 3000;

function generateNoteId(length) {
  const characters = 'abcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    const randomIndex = Math.floor(Math.random() * characters.length);
    result += characters.charAt(randomIndex);
  }
  return result;
}

let noteList = [];
let flag = process.env.FLAG;
if(!flag){
  flag='{"title":"flag","content":"bi0sctf{fake_flag}"}';
}
else{
  flag=`{"title":"flag","content":"${flag}"}`;
}
const flagid = generateNoteId(16);
const healthCheckId='Healthcheck';
fs.writeFileSync(`./notes/${flagid}.json`, flag);
fs.writeFileSync(`./notes/${healthCheckId}.json`, '{"title":"Healthcheck","content":"success"}');

app.use(express.json());

app.set('view engine', 'ejs');
app.set('views', __dirname + '/views');

const restrictToLocalhost = (req, res, next) => {
  const remoteAddress = req.connection.remoteAddress;
  if (remoteAddress === '::1' || remoteAddress === '127.0.0.1' || remoteAddress === '::ffff:127.0.0.1') {
    next();
  } else {
    res.status(403).json({ Message: 'Access denied' });
  }
};

const cleanserver = () => {
  Object.keys(require.cache).forEach(i => {
    delete require.cache[i];
  });
};

app.use('/search', restrictToLocalhost);

app.get('/delete', (req,res) => {
  cleanserver();
  return res.json({Message: 'Notes deleted successfully!'});
});

app.get('/search/:noteId', (req, res) => {
  const noteId = req.params.noteId;
  const notes=glob.sync(`./notes/${noteId}*`);
  if(notes.length === 0){
    return res.json({Message: "Not found"});
  }
  else{
    try{
      fs.accessSync(`./notes/${noteId}.json`);
      return res.json({Message: "Note found"});
    }
    catch(err){
      return res.status(500).json({ Message: 'Internal server error' });
    }
  }

})

app.get('/customise', (req, res) => {
  return res.render('customise');
});

app.post('/customise',(req, res) => {
  try {
    const { data } = req.body;

    let author = data.pop()['author'];

    let title = data.pop()['title'];

    let protoContents = fs.readFileSync('./settings.proto', 'utf-8').split('\n');

    if (author) {
      protoContents[5] = `  ${author} string author = 3 [default="user"];`;
    }

    if (title) {
      protoContents[3] = `  ${title} string title = 1 [default="user"];`;
    }

    fs.writeFileSync('./settings.proto', protoContents.join('\n'), 'utf-8');

    return res.json({ Message: 'Settings changed' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ Message: 'Internal server error' });
  }
})

app.get('/create', (req, res) => {
  return res.render('create', { noteList, Message: false });
});

app.post('/create', (req, res) => {
  requestBody=req.body
  try{
    schema = fs.readFileSync('./settings.proto', 'utf-8');
    root = protobuf.parse(schema).root;
    Note = root.lookupType('Note');
    errMsg = Note.verify(requestBody);

    if (errMsg){
      return res.json({ Message: `Verification failed: ${errMsg}` });
    }
    buffer = Note.encode(Note.create(requestBody)).finish();
    decodedData = Note.decode(buffer).toJSON();

    const noteId = generateNoteId(16);
    fs.writeFileSync(`./notes/${noteId}.json`, JSON.stringify(decodedData));
    noteList.push(noteId);

    return res.json({Message: 'Note created successfully!',Noteid: noteId });
  }
  catch (error) {
    console.error(error);
    res.status(500).json({Message: 'Internal server error' });
  }
});


app.get('/view/:noteId', (req, res) => {
  const noteId = req.params.noteId;

  try {
    let note=require.resolve(`./notes/${noteId}`);
    if(!note.endsWith(".json")){
      return res.status(500).json({ Message: 'Internal Server Error' });
    }

    let noteData = require(`./notes/${noteId}`);
    for (var key in module.constructor._pathCache) {
      if (key.startsWith("./notes/"+noteId)){
        if (!module.constructor._pathCache[key].endsWith(noteId+".json")){
          if (noteId===healthCheckId){
            cleanserver();
          }
          delete module.constructor._pathCache[key];
          return res.status(500).json({ Message: 'Internal Server Error' });
        }
      }
    }
    if(req.query.temp !== undefined){
      fs.unlink(`./notes/${noteId}.json`, (unlinkError) => {
        if (unlinkError) {
          console.error('File missing');
        }
        noteList=noteList.filter((value)=>value!=noteId);
      });
    }
    return res.render('view', { noteData });

  } catch (error) {
    console.log(error)
    return res.status(500).json({ Message: 'Internal Server Error' });
  }
});


app.get('/healthcheck',async(req,res)=>{
  try {
    await healthCheck();

    return res.json({ Message: 'healthcheck successful' });
  } catch (error) {
    console.error(error);
    return res.json({ Message: 'healthcheck failed' });
  }
});

app.get('/', (req, res) => {
  return res.redirect('/create');
});


app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal Server Error' });
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
