const notesEl = document.getElementById('notes')

let isSearch = false
let searchResults = []

if (new URLSearchParams(location.search).get('found') === '1' && location.hash) {
    searchResults = JSON.parse(atob(location.hash.slice(1)))
    isSearch = true
}

const loadNotes = (notes) => {
    if (!notes.length) {
        const noteEl = document.createElement('p')
        noteEl.textContent = 'No notes found'
        notesEl.appendChild(noteEl)
        return
    }

    notes.forEach(note => {
        if (isSearch && !searchResults.includes(note.id)) return
        const noteEl = document.createElement('p')
        noteEl.textContent = note.text
        notesEl.appendChild(noteEl)
    })
}

fetch('/notes')
    .then(res => res.json())
    .then(notes => loadNotes(notes))

