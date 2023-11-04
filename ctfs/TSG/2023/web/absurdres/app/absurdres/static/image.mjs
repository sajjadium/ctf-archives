document.addEventListener('DOMContentLoaded', () => {
	for (const button of document.querySelectorAll('button.copy')) {
		button.addEventListener('click', () => {
			const text = button.previousSibling.previousSibling.textContent;
			navigator.clipboard.writeText(text);
			button.innerHTML = `Copied ${text}`;
		});
	}
});