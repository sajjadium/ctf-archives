let preview = document.getElementById("preview"),
	save = document.getElementById("save"),
	textarea = document.getElementById("input-area"),
	frame = document.getElementById("frame-area"),
    status = document.getElementById("status"), 
	token = undefined; 

alert = function(msg) {
    status.innerText = "Info: " + msg; 
}

preview.onclick = function() {
    console.log("Sending Preview..")
	frame.contentWindow.postMessage(textarea.value, `http://${document.location.host}/`); 
	return false;
}

save.onclick = function() {
	if (token == undefined)
	{
		alert("Preview before saving!")
	} else {
		fetch("/api/create", {
			method: "POST",
			credentials: "include",
			body: JSON.stringify({
				Hash: token,
				Raw: textarea.value
			})
		}).then(resp => resp.json())
		.then(response => {
            if (response["Status"] != "success") {
                alert("Could not save markdown.")
            } else {
                alert("Saved post to : " + response["Bucket"] + "/" + response["PostId"])
                frame.src = `http://${document.location.host}/${response['Bucket']}/${response["PostId"]}`
            }
			console.log(response)
			token = undefined
		}); 
	}
	return false; 
}

window.addEventListener("message", (event) => {
	if (event.origin != window.origin)
	{
		console.log("Error");
		return false;
	}
    data = event.data
	textarea.value = data["Raw"]
	token = data["Hash"]
});
