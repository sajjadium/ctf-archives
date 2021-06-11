var safeTags = ["a","b","em","ul","span","nav","i","u","input","img","noscript","p","div"];
var safeAttributes = ["id","height","width","src","href"];

var getp = (n,d)=>(new URLSearchParams(document.location.search).get(n)||d);
var customFilter = (unsafe)=>{
	const safeTemplate = document.createElement("template");
	if(support_trusted()){
		safeTemplate.innerHTML = window.policy.createHTML(unsafe);
	} else {
		safeTemplate.innerHTML = unsafe;
	}

	var els = safeTemplate.content.querySelectorAll("*");
	for(var el of els){
		if(!safeTags.includes(el.tagName.toLowerCase())) el.remove();
		var attrs = el.attributes;
		for(var attr of attrs){
			if(!safeAttributes.includes(attr.name.toLowerCase())) el.removeAttribute(attr.name);
		}
	}
	return safeTemplate.innerHTML;
}

var copyObjs = (to,from)=>{
	for(var prop in from){
		if(typeof from[prop] == "object"){
			if(!to[prop]) to[prop] = Object.create(null);
			copyObjs(to[prop],from[prop]);
		} 
		else to[prop] = from[prop];
	}
}

var niceFeature = ()=>{
	var wow = getp("wow","{}");
	wow = JSON.parse(wow);
	var n = Object.create(null);
	n.name = "nothing";
	copyObjs(n,wow);
	if(n.name == "ram") alert("What a nice name!");
}

var support_trusted = ()=>{
	if(window.support_trusted_types != undefined){
		return window.support_trusted_types == true;
	}

	try{
		trustedTypes.createPolicy('default', {
    		createHTML: (input) => input,
    		createScriptURL: (input) => input,
			createScript: (input)=>input
  		});

		if(!Object.getOwnPropertyNames(window).includes("trustedTypes")){
			throw 1337;
		}
		window.support_trusted_types = true;
		return true;
	} catch(e){
		window.support_trusted_types = false;
  		return false;
	}
}
	
(function(){
	try{
		niceFeature();
	} catch(e){
		console.log(e);
	}

	var unsafe = getp("name","Guest")

	if(support_trusted()){
		window.policy = trustedTypes.createPolicy('safe', {
			createHTML: (input) => DOMPurify.sanitize(input),
			createScriptURL: (input) => input,
			createScript: (input)=>input
		});
	}

	var safe = customFilter(unsafe);

	if(support_trusted()){
		document.getElementById("vname").innerHTML = policy.createHTML(safe);
	} else {
		document.getElementById("vname").innerHTML = safe;
	}
})()

