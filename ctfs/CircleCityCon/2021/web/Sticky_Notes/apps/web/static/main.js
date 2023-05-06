const id = window.location.pathname.split('/')[2]
if (!/^[a-z0-9-/]+$/.test(id)) {
  alert('Invalid board ID')
  throw new Error('Invalid board ID')
}

const notesDiv = document.getElementById('notes')
const notesPlaceholder = document.getElementById('notes-placeholder')
const noteTextarea = document.getElementById('note-textarea')
const form = document.getElementById('add-note-form')
const reportButton = document.getElementById('report-button')
const reportIcon = document.getElementById('report-icon')

function addNote (note) {
  notesPlaceholder.hidden = true
  const iframe = document.createElement('iframe')
  iframe.src = `http://35.224.135.84:3101/${id}/${note}`
  notesDiv.appendChild(iframe)
}

form.addEventListener('submit', async (event) => {
  event.preventDefault()
  const formData = new FormData(event.target)
  const reqData = Object.fromEntries(formData.entries())
  reqData.id = id
  const res = await fetch('/board/add_note', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(reqData)
  })

  const resData = await res.json()
  res.status === 200 ? addNote(resData) : alert(JSON.stringify(resData))
  noteTextarea.focus()
})

reportButton.addEventListener('click', async (_) => {
  reportIcon.textContent = 'pending'
  const res = await fetch(`/board/${id}/report`)
  const resData = await res.json()
  if (res.status === 200) {
    reportIcon.textContent = 'done'
  } else {
    alert(JSON.stringify(resData))
    reportIcon.textContent = 'error'
  }
})

async function fetchNotes() {
  const res = await fetch(`/board/${id}/notes`)
  const notes = await res.json()
  if (res.status !== 200) {
    alert(JSON.stringify(notes))
    return
  }

  for (const note of notes) {
    addNote(note)
  }
}

fetchNotes()
