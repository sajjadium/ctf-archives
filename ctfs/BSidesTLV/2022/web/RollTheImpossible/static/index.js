function step(){
	var server_data = {}
	fetch("/step", {
		"method": "POST",
		"headers": {"Content-Type": "application/json"},
		"body": JSON.stringify(server_data)
	})
	.then(response => response.json())
	.then(data => {
		document.getElementById("new_digit").textContent = data["new_digit"]
		document.getElementById("num").textContent = data["num"]
		if (data["flag"] != "") {
			alert(data["flag"])
		}
	})
}
