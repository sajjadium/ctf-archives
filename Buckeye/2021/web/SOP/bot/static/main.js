const form = document.getElementById('form')
const submit = document.getElementById('submit')
const submitIcon = submit.firstElementChild

form.addEventListener('submit', async (event) => {
  event.preventDefault()

  submit.className = 'submit'
  submit.classList.add('pending')
  submitIcon.textContent = 'pending'

  const formData = new FormData(event.target)
  const reqData = Object.fromEntries(formData.entries())
  const res = await fetch('/visit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(reqData)
  })

  submit.className = 'submit'
  if (res.status === 200) {
    submit.classList.add('success')
    submitIcon.textContent = 'done'
  } else {
    submit.classList.add('error')
    submitIcon.textContent = 'error'
    const data = await res.json()
    alert(data.error)
  }
})
