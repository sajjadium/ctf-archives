function updateTask(taskCard) {
	stopEditingStyle(taskCard);

	fetch("/api/manage_tasks", {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify({
			task: taskCard.querySelector(".task").innerText,
			status: taskCard.querySelector(".status").innerText
		})
	})
}

function stopEditingStyle(taskCard) {
	taskCard.classList.remove("editable");
	let task = taskCard.querySelector(".task");
	let status = taskCard.querySelector(".status");
	taskCard.querySelector(".edit").innerText = "✎";

	status.contentEditable = false;
	status.style.fontWeight = "normal";
	status.style.cursor = "inherit";
}

function completeTaskStyle(taskCard) {
	taskCard.querySelector(".status").innerText = "Completed";
	taskCard.querySelector(".task-container").style.textDecoration = "line-through";
	taskCard.querySelector(".edit").hidden = true;
	taskCard.querySelector("input[type=checkbox]").checked = true;
}

window.addEventListener("load", async () => {
	await fetch("/api/get_tasks", { method: "POST" })
		.then(r => r.json())
		.then(tasks => {
			for (const [task, status] of Object.entries(tasks)) {
				let card = document.createElement("article");
				card.className = "task-card";

				let checkbox = document.createElement("input");
				checkbox.type = "checkbox";

				let container = document.createElement("div");
				container.className = "task-container";

				let taskEl = document.createElement("span");
				taskEl.innerText = task.replaceAll("\n", "");
				taskEl.className = "task";

				let statusEl = document.createElement("em");
				statusEl.innerText = status ? status.replaceAll("\n", "") : "";
				statusEl.className = "status";

				let editButton = document.createElement("a");
				editButton.classList.add("edit");
				editButton.innerText = "✎";	

				// this breaks stuff, sorry :(
				statusEl.addEventListener("paste", e => e.preventDefault());
				statusEl.addEventListener("keypress", e => {
					if (e.target.textContent.length >= 50) e.preventDefault();
					if (e.charCode === 13) {
						e.preventDefault();
						updateTask(e.target.parentNode.parentNode);
					}
				})

				container.append(taskEl, statusEl);
				card.append(checkbox, container, editButton);

				if (status === false) {
					completeTaskStyle(card);
					document.querySelector("#completed-tasks").appendChild(card);
				}
				else document.querySelector("#ongoing-tasks").appendChild(card);
			}
		});

	document.querySelector("#section-completed").hidden = false;

	document.querySelectorAll("input[type=checkbox]").forEach(el => {
		el.addEventListener("click", e => {
			let taskCard = e.target.parentNode;
			let newParent;
			taskCard.classList.add("shrink");

			if (e.target.checked) {
				newParent = document.querySelector("#completed-tasks");
				fetch("/api/manage_tasks", {
					method: "POST",
					headers: { "Content-Type": "application/json" },
					body: JSON.stringify({
						task: taskCard.querySelector(".task").innerText
					})
				})
			} else {
				newParent = document.querySelector("#ongoing-tasks");
				fetch("/api/manage_tasks", {
					method: "POST",
					headers: { "Content-Type": "application/json" },
					body: JSON.stringify({
						task: taskCard.querySelector(".task").innerText,
						status: "In progress"
					})
				})
			}

			setTimeout(() => {
				if (e.target.checked) {
					completeTaskStyle(taskCard);
					stopEditingStyle(taskCard);
				}
				else {
					taskCard.querySelector(".status").innerText = "In progress";
					taskCard.querySelector(".task-container").style.textDecoration = "none";
					taskCard.querySelector(".edit").hidden = false;
				}

				taskCard.remove();
				newParent.firstElementChild.after(taskCard);
				taskCard.classList.remove("shrink");
			}, 250);

		})
	});

	document.querySelectorAll(".edit").forEach(el => {
		el.addEventListener("click", e => {
			let taskCard = e.target.parentNode;
			let task = taskCard.querySelector(".task");
			let status = taskCard.querySelector(".status");
			taskCard.querySelector(".edit").innerText = "Done";

			if (!taskCard.classList.contains("editable")) {

				status.contentEditable = true;
				status.style.fontWeight = "bold";
				status.style.cursor = "text";
				status.focus();

				taskCard.classList.add("editable");
			} else {
				updateTask(taskCard);
			}
		})
	})
})