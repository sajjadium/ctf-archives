const express = require('express');
const deparam = require('jquery-deparam');
const {template} = require('./util.js');
const pug = require('pug');
const child_process = require('child_process');


const app = express()
const port = 3000

app.set('view engine', 'pug')
//Configure server-staus options here
options = {args:["-eo", "cpu,args"], options:{"timeout":500} }
//I don't trust these modules
Object.seal && [ Object, Array, String, Number ].map( function( builtin ) { Object.seal( builtin.prototype ); } )
//I believe in Defense in Depth and I don't trust the code I write, so here is my waf
app.use((req, res, next) => {
	inp = decodeURIComponent(req.originalUrl)
	const denylist = ["%","(","global", "process","mainModule","require","child_process","exec","\"","'","!","`",":","-","_"];
	for(i=0;i<denylist.length; i++){
		if(inp.includes(denylist[i])){
			return res.send('request is blocked');
		}
	}

	next();
  });
  

app.get('/',(req,res) =>{
	var basic = {
		title: "Pug 101",
		head: "Welcome to Pug 101",
		name: "Guest"
	}
	var input = deparam(req.originalUrl.slice(2));
	if(input.name)
		basic.name = input.name.Safetify()
	if(input.head)
	    basic.head = input.head.Safetify()
	var content = input.content? input.content.Safetify() : ''
	var pugtmpl = template.replace('OUT',content)
	const compiledFunction = pug.compile(pugtmpl)
	res.send(compiledFunction(basic));
});

app.get('/serverstatus', (req, res) => {
	const result = child_process.spawnSync('ps' , options.args, options.options);
	out = result.stdout.toString();
	res.send(out)
})

app.listen(port, () => {
  console.log('started')
})
