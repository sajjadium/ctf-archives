Module.onRuntimeInitialized = async (_) => {
    const api = {
        sanitize: Module.cwrap('sanitize', 'string', ['string']),
    };
    const note = new URLSearchParams(window.location.search).get('note');

    if (note) {
        if (note.length > 50) {
            alert('Note is too long');
            window.location = '/';
        }
        else {
            const sanitized = api.sanitize(note.toLowerCase());
            document.getElementById('note-text').innerHTML = sanitized;
        }
    }
};