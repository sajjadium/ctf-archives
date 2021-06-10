
var meta = document.createElement('meta');
meta.setAttribute('http-equiv', 'Content-Security-Policy');
meta.setAttribute('content', "default-src 'none'; img-src 'self';script-src 'self'; style-src 'self'");
document.getElementsByTagName('head')[0].appendChild(meta);
