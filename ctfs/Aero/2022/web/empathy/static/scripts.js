const sections = {
    login: document.getElementById('section-login'),
    index: document.getElementById('section-index'),
    note: document.getElementById('section-note'),
};

const errors = {
    login: document.getElementById('error-login'),
    index: document.getElementById('error-index'),
};

const inputs = {
    username: document.getElementById('input-username'),
    password: document.getElementById('input-password'),
    noteId: document.getElementById('input-note-id'),
    noteTitle: document.getElementById('input-note-title'),
    noteText: document.getElementById('input-note-text'),
};

const forms = {
    login: document.getElementById('form-login'),
    logout: document.getElementById('form-logout'),
    showNote: document.getElementById('form-show-note'),
    createNote: document.getElementById('form-create-note'),
    closeNote: document.getElementById('form-close-note'),
};

const infos = {
    username: document.getElementById('info-username'),
    noteId: document.getElementById('info-note-id'),
    noteTitle: document.getElementById('info-note-title'),
    noteText: document.getElementById('info-note-text'),
};


async function apiLogin(username, password) {
    const response = await fetch(`/api/login/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username,
            password: password,
        }),
    });

    switch (response.status) {
        case 200:
            return await response.json();

        case 400:
            throw Error('incorrect password');

        default:
            throw Error('unknown error');
    }
}

async function apiProfile() {
    const response = await fetch(`/api/profile/`, {
        method: 'GET',
    });

    switch (response.status) {
        case 200:
            return await response.json();

        case 401:
            throw Error('auth failed');

        default:
            throw Error('unknown error');
    }
}

async function apiLogout() {
    const response = await fetch(`/api/logout/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    switch (response.status) {
        case 200:
            return;

        case 401:
            throw Error('auth failed');

        default:
            throw Error('unknown error');
    }
}

async function apiCreateNote(title, text) {
    const response = await fetch(`/api/note/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            title: title,
            text: text,
        }),
    });

    switch (response.status) {
        case 200:
            return await response.json();

        case 401:
            throw Error('auth failed');

        default:
            throw Error('unknown error');
    }
}

async function apiShowNote(noteId) {
    const response = await fetch(`/api/note/${noteId}/`, {
        method: 'GET',
    });

    switch (response.status) {
        case 200:
            return await response.json();

        case 401:
            throw Error('auth failed');

        case 403:
            throw Error('you have no access to this note');

        case 404:
            throw Error('note is not found');

        default:
            throw Error('unknown error');
    }
}


async function doLogin() {
    errors.login.innerText = '';
    let user;

    try {
        user = await apiLogin(
            inputs.username.value,
            inputs.password.value,
        );
    }
    catch (error) {
        errors.login.innerText = error.message;
        return;
    }

    infos.username.innerText = user.username;

    sections.login.hidden = true;
    sections.index.hidden = false;

    inputs.username.value = '';
    inputs.password.value = '';
}

async function doLogout() {
    errors.index.innerText = '';

    try {
        await apiLogout();
    }
    catch (error) {
        errors.index.innerText = error.message;
        return;
    }

    sections.index.hidden = true;
    sections.login.hidden = false;

    infos.username.innerText = '';
}

async function doCreateNote() {
    errors.index.innerText = '';
    let note;

    try {
        note = await apiCreateNote(
            inputs.noteTitle.value,
            inputs.noteText.value,
        );
    }
    catch (error) {
        errors.index.innerText = error.message;
        return;
    }

    inputs.noteId.value = note.id;

    await doShowNote();

    inputs.noteTitle.value = '';
    inputs.noteText.value = '';
}

async function doShowNote() {
    errors.index.innerText = '';
    let note;

    try {
        note = await apiShowNote(inputs.noteId.value);
    }
    catch (error) {
        errors.index.innerText = error.message;
        return;
    }

    infos.noteId.innerText = inputs.noteId.value;
    infos.noteTitle.innerText = note.title;
    infos.noteText.innerText = note.text;

    sections.index.hidden = true;
    sections.note.hidden = false;

    inputs.noteId.value = '';
}

async function doCloseNote() {
    sections.note.hidden = true;
    sections.index.hidden = false;

    infos.noteId.innerText = '';
    infos.noteTitle.innerText = '';
    infos.noteText.innerText = '';
}


async function checkSession() {
    let user;

    try {
        user = await apiProfile();
    }
    catch (error) {
        return;
    }

    infos.username.innerText = user.username;

    sections.login.hidden = true;
    sections.index.hidden = false;
}

async function init() {
    forms.login.addEventListener('submit', async event => {
        event.preventDefault();
        await doLogin();
    });
    forms.logout.addEventListener('submit', async event => {
        event.preventDefault();
        await doLogout();
    });

    forms.createNote.addEventListener('submit', async event => {
        event.preventDefault();
        await doCreateNote();
    });
    forms.showNote.addEventListener('submit', async event => {
        event.preventDefault();
        await doShowNote();
    });
    forms.closeNote.addEventListener('submit', async event => {
        event.preventDefault();
        await doCloseNote();
    });

    sections.index.hidden = true;
    sections.note.hidden = true;
    sections.login.hidden = false;
    
    await checkSession();
}

init();
