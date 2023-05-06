window.SETTINGS = window.SETTINGS || [{
  dataset:{
    "timezone":"",
    "location":"Tunisia"
  },
  Title:"FwordFeedbacks",
  check: false	
}]
function looseJsonParse(obj){
  if(obj.length<35){  
	return eval("(" + obj + ")");
  }else{
    return {location:"Limit Length Exceeded"}
  }
}
function addInfos(){
	if(window.showInfos && SETTINGS.check  && SETTINGS[0].dataset.timezone.length>2){
        var infos=`{location:${SETTINGS[0].dataset.location}}`;
	var result=document.createElement("p");
	result.textContent=`Location: ${looseJsonParse(infos).location} Timezone: UTC+1` ;
	document.getElementById("out").appendChild(result);
	console.log(result);
	}
}
addInfos()
