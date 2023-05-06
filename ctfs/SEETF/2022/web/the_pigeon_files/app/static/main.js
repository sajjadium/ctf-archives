const noteForm = document.getElementById("note");
const output = document.getElementById("output");

const uuidv4 = () => {
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}

noteForm.onsubmit = (e) => {
    e.preventDefault();
    window.localStorage.setItem("note", new FormData(noteForm).get("note"));

    const uuid = uuidv4();
    window.localStorage.setItem("uuid", uuid);

    Swal.fire(
        'Viva La Resistance',
        `Here's your personal token: ${uuid}. You will need this to retrieve your note.`,
        'success'
    )
};

const search = (request) => {
    const uuid = window.localStorage.getItem("uuid");
    const note = window.localStorage.getItem("note");

    if (!uuid || !note) {
        Swal.fire(
            'Not found',
            'You need to submit a note first.',
            'error'
        )
        return null;
    }
    
    if (note.startsWith(request.search)) {
        request.result = note;
    }
    else {
        request.result = null;
    }
    
    if (request.token === uuid) {
        request.accessGranted = true;
    }

    return request;
};

// Search for notes
if (location.search) {

    // MooTools awesome query string parsing
    request = String.parseQueryString(location.search.slice(1));
    request = search(request);

    if (request) {
        if (!request.accessGranted) {
            output.textContent = "Access denied.";
        }
        else if (!request.result) {
            output.textContent = "Note not found.";
        }
        else {
            output.textContent = request.result;
            setTimeout(() => {window.location.search = ""}, 5000);
        }
    }
}