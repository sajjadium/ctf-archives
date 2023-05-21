const express = require('express');
const bodyParser = require('body-parser');
const ejs = require('ejs');
const hash = require('crypto-js/md5');
const fs = require('fs');
const app = express();


var letter = {};
var read = {};
function isObject(obj) {
	return obj !== null && typeof obj === 'object';
}
function setValue(obj, key, value) {
	const keylist = key.split('.');
	const e = keylist.shift();
	if (keylist.length > 0) {
		if (!isObject(obj[e])) obj[e] = {};
		setValue(obj[e], keylist.join('.'), value);
	} else {
		obj[key] = value;
		return obj;
	}
}

app.use(bodyParser.urlencoded({ extended: false }));
app.set('view engine', 'ejs');


app.get('/', function (req, resp) {
	read['lettername'] = 'crush';
	resp.render(__dirname + "/ejs/index.ejs");
})


app.post('/sendcrush',function(req,resp){
	let {name , crush ,content}=req.body;
	lettername=hash(crush).toString();
	content = name + " sent you a letter: " + content;
	fs.writeFile(__dirname+"/myletter/"+lettername,content,function(err){
		if(err==null){
			letter[lettername]=lettername;
			resp.send(`I will send this message to your crush, hoping that she will read it <3
						Your letter name is : ${lettername}`);
		}else{
			resp.write("<script>alert('hack cc')</script>");
			resp.write("<script>window.location='/'</script>");
		}
	})

})
// flag in flag.txt
app.get('/readletter', function (req, resp) {
	let lettername = letter[req.query.lettername];
	if (lettername == null) {
		fs.readFile(__dirname + '/myletter/' + read['lettername'], 'UTF-8', function (err, data) {
			resp.send(data);
		})
	}
	else {
		read[lettername] = lettername;
		fs.readFile(__dirname + '/myletter/' + read[lettername], 'UTF-8', function (err, data) {
			if (err == null) {
				resp.send(data);
			} else {
				resp.send('letter is not existed');
			}
		})
	}

})

app.get('/hacking', function (req, resp) {
	let { hack, lettername, rename } = req.query;
	if (hack == null) {
		resp.send('Don\'t try to hack anything, she doesn\'t love you.');
	} else if (hack == 'rename') {
		setValue(letter, lettername, rename)
		resp.send('Nice !!!!!!!');
	} else if (hack == 'reset') {
		read = {};
		resp.send("All letter have been deleted");
	}
})

app.listen(1301);

console.log("listen on 0.0.0.0:1301");