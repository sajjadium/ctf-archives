const search_form = document.getElementById("search-form");
const search_input = document.getElementById("search");
const items = document.getElementById("items");

search_form.addEventListener("submit", function (event) {
	event.preventDefault();
	search(search_input.value);
});

async function search(val) {
	let resp = await fetch("/api/search", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ search: val }),
	});

	let { error, results } = await resp.json();

	if (error) {
		items.textContent = error;
		return;
	}

	items.innerHTML = "";
	for (let { challenge, price } of results) {
		let row = document.createElement("tr");

		let chall_cell = document.createElement("td");
		chall_cell.textContent = challenge;

		let price_cell = document.createElement("td");
		price_cell.textContent = `$${price}.00`;

		let buy_cell = document.createElement("td");
		let buy_button = document.createElement("button");
		buy_button.textContent = "Buy Flag";
		buy_button.addEventListener("click", function () {
			alert("Not implemented yet!");
		});
		buy_cell.append(buy_button);

		row.append(chall_cell, price_cell, buy_cell);
		items.append(row);
	}
}

search("");
