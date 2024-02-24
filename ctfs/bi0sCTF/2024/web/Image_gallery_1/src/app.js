const express = require('express');
const cookieParser = require('cookie-parser');
const fs = require('fs');
const ejs = require('ejs');
const path = require("path"); 
const fileUpload = require('express-fileupload');
const {randomUUID } =  require("crypto");
const { visit } = require('./bot');
const flag_id = randomUUID();
const maxSizeInBytes = 3 * 1024 * 1024;


const plantflag = () => {

  fs.mkdirSync(path.join(__dirname,`/public/${flag_id}`))
  fs.writeFileSync(path.join(__dirname,`/public/${flag_id}/flag.txt`),process.env.FLAG||'flag{asdf_asdf}')

}


const app = express();

app.set('view engine', 'ejs');
app.use(express.static('public'));
app.use(cookieParser());
app.use(fileUpload());
app.use(express.json())


app.get('/', async(req, res) => {

  if(req.cookies.sid && /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/.test(req.cookies.sid)){

    try {

      const files = btoa(JSON.stringify(fs.readdirSync(path.join(__dirname,`/public/${req.cookies.sid}`))));
      return res.render('index', {files: files,id : req.cookies.sid});
  
    } catch (err) {}  
  }

  let id = randomUUID();
  fs.mkdirSync(path.join(__dirname,`/public/${id}`))
  res.cookie('sid',id,{httpOnly: true}).render('index', {files: null, id: id});
  return;

  
  
});

app.post('/upload',async(req,res) => {

  if (!req.files || !req.cookies.sid) {
    return res.status(400).send('Invalid request');
  }
    try{
      const uploadedFile = req.files.image;
      if (uploadedFile.size > maxSizeInBytes) {
        return res.status(400).send('File size exceeds the limit.');
      }
      await uploadedFile.mv(`./public/${req.cookies.sid}/${uploadedFile.name}`);
   }catch{
      return res.status(400).send('Invalid request');
   }

  res.status(200).redirect('/');
  return
})

app.post('/share',async(req,res) => {

  let id = req.body.id
  await visit(flag_id,id);
  res.send('Sucess')
  return

})

const port = 3000;
app.listen(port, () => {
  plantflag()
  console.log(`Server is running on port ${port}`);
});