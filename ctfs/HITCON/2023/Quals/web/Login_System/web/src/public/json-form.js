class JsonForm extends HTMLFormElement {
	constructor() {
		super()
		this.addEventListener('submit', e => {
			e.preventDefault()
			const data = Object.fromEntries(new FormData(this).entries())
			fetch(this.action, {
				headers: {
					'Content-Type': 'application/json'
				},
				method: this.method,
				body: JSON.stringify(data)
			})
				.then(r => r.json())
				.then(r => {
					if (r.success) {
						location.href = this.dataset.success
					} else {
						alert(r.error)
					}
				})
				.catch(e => {
					alert(e.message)
				})
		})
	}
}

customElements.define('json-form', JsonForm, {
	extends: 'form'
})
