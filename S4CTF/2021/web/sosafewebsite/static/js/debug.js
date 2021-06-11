if(window.used == undefined){
	window.used = true;
	window.debugparams = {}
	window.debugparams.soallowedTags = ["a","b","em","ul","span","nav","i","u","input","img","noscript","p","div","iframe"];
	var debugopts = window.debugOptions || [[{"clear":"globalThis"},{"face":"safeTags"},{"code":"debugparams"},{"accept":"soallowedTags"}]];
	if(debugopts.length == 1){
		var settings = debugopts[0];
		window[settings[0].clear][settings[1].face] = window[settings[2].code][settings[3].accept];
	};
}
