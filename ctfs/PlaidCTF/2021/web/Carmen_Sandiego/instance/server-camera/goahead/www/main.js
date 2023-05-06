window.onload = async () => {
	let res = await fetch("/cgi-bin/latest");
	let data = await res.json();

	for (let camera of Object.keys(data.cameras)) {
		let cameraElement = document.createElement("div");
		cameraElement.className = "camera";

		let valueElement = document.createElement("img");
		valueElement.className = "value";
		valueElement.src = data.cameras[camera];
		cameraElement.appendChild(valueElement);

		let nameElement = document.createElement("div");
		nameElement.className = "name";
		nameElement.innerText = camera;
		cameraElement.appendChild(nameElement);

		let restartElement = document.createElement("div");
		restartElement.className = "restart";
		restartElement.innerHTML = "&#x21BB;";
		restartElement.title = "Restart Camera";
		restartElement.addEventListener("click", async () => {
			restartElement.innerText = "...";
			await fetch("/cgi-bin/restart?camera=" + camera, { method: "POST" });
			restartElement.innerHTML = "&#x21BB;";
		});
		cameraElement.appendChild(restartElement);

		document.getElementById("camera-list").appendChild(cameraElement);
	}
};
