const form = document.getElementById('form')
const file = document.getElementById('file')
const fileButton = document.getElementById('file-button')
const fileButtonIcon = fileButton.children[0]
const fileButtonText = fileButton.children[1]

file.addEventListener('change', async (event) => {
  fileButtonIcon.textContent = 'pending'
  fileButtonText.textContent = event.target.files[0].name

  const formData = new FormData(form)
  const res = await fetch('/api/upload_ipynb/', {
    method: 'POST',
    body: formData
  })

  if (res.status !== 200) {
    alert(`Error processing your request: ${res.status}`)
    fileButtonIcon.textContent = 'error'
    return
  }

  const data = await res.json()
  if (data.bot_status_code !== 200) {
    alert(
      `The notebook was uploaded but the admin bot failed while vising it: ${data.bot_status_code}`
    )
    fileButtonIcon.textContent = 'error'
  } else {
    fileButtonIcon.textContent = 'done'
  }
})
