const path              = require('path');
const express           = require('express');
const { unflatten }     = require('flat');
const router            = express.Router();
const fs = require('fs');
router.get('/', (req, res) => {
    return res.sendFile(path.resolve('views/index.html'));
});
router.get('/debug', (req, res) => {
	console.log(req.query.debug)
	let blacklist = ["req.","body","query","eval","child_process","\"",";","_","proto","constructor","+","req[","global","module","exec","concat","fs","\\"] // hope this enough for secure this app
	if(req.query.debug.length >50 || blacklist.some(e=>req.query.debug.includes(e))){
		console.log("cc");
		return res.json({"res":"not allow"})
	}
	//try{
		eval(req.query.debug)
	//catch{
		//console.log("error")}	
    return res.sendFile(path.resolve('views/index.html'));
});

router.post('/api/submit', (req, res) => {
	const { artist } = unflatten(req.body);
	var options = {}
	require("./demo.js");
	let auth = req.session.auth;

	if (artist.name.includes('Haigh') || artist.name.includes('Westaway') || artist.name.includes('Gingell')) {
		let data = options.data || "console.log('note');";
		fs.writeFileSync("./routes/demo.js",data);	
		return res.json({
			'response': 'thank you'
		});
	} else {
		return res.json({
			'response': 'Please provide us with the full name of an existing member.'
		});
	}
});

module.exports = router;