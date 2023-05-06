const form = document.getElementById('form')
const submissionStatus = document.getElementById('status')

form.addEventListener('submit', async (event) => {
  event.preventDefault()
  
  submissionStatus.classList.add('alert-primary')
  submissionStatus.textContent = 'Pending...'

  const formData = new FormData(event.target)
  const reqData = Object.fromEntries(formData.entries())
  const res = await fetch('/visit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(reqData)
  })

  let success = false

  if (res.status === 200) {
    success = true
    submissionStatus.textContent = 'Done'
  } 
  else {
    const data = await res.json()
    submissionStatus.textContent = `Error: ${data.error}`
  }

  submissionStatus.classList.remove('alert-primary')
  submissionStatus.classList.toggle('alert-success', success)
  submissionStatus.classList.toggle('alert-danger', !success)
})
