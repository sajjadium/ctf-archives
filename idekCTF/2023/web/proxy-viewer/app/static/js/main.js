const submitForm = () => {
	const form = document.getElementById("proxyForm");
	let url = form[0].value;
	form.action = `${window.location.origin}/proxy/${encodeURIComponent(url)}`;
	form.submit()
};
