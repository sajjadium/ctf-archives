window.onload = async () => {
	let res = await fetch("/cgi-bin/latest");
	let data = await res.json();

	for (let sensor of Object.keys(data.sensors)) {
		let sensorElement = document.createElement("div");
		sensorElement.className = "sensor";

		let valueElement = document.createElement("div");
		valueElement.className = "value";
		valueElement.innerText = data.sensors[sensor].value;
		sensorElement.appendChild(valueElement);

		let nameElement = document.createElement("div");
		nameElement.className = "name";
		nameElement.innerText = sensor;
		sensorElement.appendChild(nameElement);

		let restartElement = document.createElement("div");
		restartElement.className = "restart";
		restartElement.innerHTML = "&#x21BB;";
		restartElement.title = "Restart Sensor";
		restartElement.addEventListener("click", async () => {
			restartElement.innerText = "...";
			await fetch("/cgi-bin/restart?sensor=" + sensor, { method: "POST" });
			restartElement.innerHTML = "&#x21BB;";
		});
		sensorElement.appendChild(restartElement);

		document.getElementById("sensor-list").appendChild(sensorElement);
	}
};
