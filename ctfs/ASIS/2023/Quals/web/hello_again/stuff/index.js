const path = require('path');
const crypto = require('crypto');
const isPrivate = p=>{
	pbase = path.basename(p);
	return p.indexOf('private') > -1 || /%|private/.test(pbase);
}

const router = new Bun.FileSystemRouter({
  style: 'nextjs',
  dir: '/app/cgi-bin/',
  origin: 'https://asisctf.com/',
  assetPrefix: '/cgi-bin/'
});

const secretToken = 'Bearer '+crypto.randomBytes(16).toString('base64') 

const server = Bun.serve({
  port: 8000,
  fetch(req) {
  	let url = new URL(req.url);
  	let pname = url.pathname;
  	if(pname.startsWith('/cgi-bin/')){
  		pname = pname.slice('/cgi-bin/'.length-1);
	  	try{ pname = decodeURIComponent(pname) }catch(e){}

	  	if(isPrivate(pname) && secretToken != req.headers.get('Authorization')){
	  		return Response('Bad script');
	  	}

	  	let r = router.match(pname);
	  	if(r){
	  		try{
		  		return new Response(require(r.filePath).request(url.searchParams));
	  		} catch(e){
	  			return new Response('Error.');
	  		}
	  	}
  	} else if(pname == '/'){
  		return new Response('wow take a look: /cgi-bin/sayhi?name=hacker')
  	}
		return new Response("Not Found.");
  }
});
