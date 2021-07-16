var express = require('express');
var app = express();
var http = require('http').createServer(app);
var io = require('socket.io')(http);
var md5 = require("md5");
var fs = require('fs');

const flag = fs.readFileSync("flag.txt",{encoding:'utf8', flag:'r'});

var accounts = {};
// Special account for LIT Organizers
var admin_id = Math.floor(Math.random() * 1000)
accounts[flag] = {
	"password": md5(flag),
	"rand_id": admin_id
};

id2Name = {};
for(let [name,account] of Object.entries(accounts)) {
	id2Name[account["rand_id"]] = name;
}

io.on('connection',(socket) => {
	socket.on('login',(tn,pwd) => {
		if(accounts[tn] == undefined || accounts[tn]["password"] != md5(pwd)) {
			socket.emit("loginRes",false,-3);
			return;
		}
		socket.emit("loginRes",true,accounts[tn]["rand_id"]);
		return;
	});

	socket.on('reqName',(rand_id) => {
		name = id2Name[parseInt(rand_id)];
		socket.emit("reqNameRes",name);
	});

	socket.on('register',(tn,pwd) => {
		if(accounts[tn] != undefined) {
			socket.emit("regRes",false,-1);
			return;
		}
		if(Object.keys(accounts).length >= 500) {
			socket.emit("regRes",false,-2);
			return;
		}
		var rand_id = Math.floor(Math.random() * 1000);
		while(id2Name[rand_id] != undefined) {
			rand_id = Math.floor(Math.random() * 1000);
		}
		accounts[tn] = {
			"password": md5(pwd),
			"rand_id": rand_id
		};
		id2Name[rand_id] = tn;
		socket.emit("regRes",true,rand_id);
	});
});


app.get('/',(req,res) => {
	res.sendFile(__dirname + '/html/index.html');
});

app.get('/login',(req,res) => {
	res.sendFile(__dirname + '/html/login.html');
});

app.get('/register',(req,res) => {
	res.sendFile(__dirname + '/html/register.html');
});

app.get('/contest',(req,res) => {
	res.sendFile(__dirname + '/html/contest.html');
});

http.listen(8081,() => {
	console.log('listening on *:8081');
});
