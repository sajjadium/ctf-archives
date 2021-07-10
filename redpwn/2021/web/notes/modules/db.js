class Database {
  constructor() {
    // username -> password
    this.passwords = new Map();

    // username -> notes
    this.notes = new Map();
  }

  register(username, password) {
    this.passwords.set(username, password);
    this.notes.set(username, []);
  }

  getPassword(username) {
    return this.passwords.get(username);
  }

  getNotes(username) {
    return this.notes.get(username);
  }

  addNote(username, note) {
    this.notes.get(username).push(note);
  }
}

module.exports = Database;
