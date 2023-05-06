const mail = new Map();

function createUser(email, password) {
    if (mail.has(email)) throw new Error('User already exists');

    mail.set(email, new Map([
        ['mail', []],
        ['password', password]
    ]));
}

function getUser(email) {
    if (mail.has(email)) {
        return mail.get(email);
    }

    return null;
}

function addEmail(email, message) {
    if (!mail.has(email)) throw new Error('Email not found');
    
    let inbox = mail.get(email).get('mail'); 
    inbox.push(message);

    if (inbox.length > 10) {
        inbox.shift();
    }
}


export {
    createUser,
    getUser,
    addEmail
}