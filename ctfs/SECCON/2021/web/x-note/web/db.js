const crypto = require("crypto");

class Db {
  constructor() {
    this.idToUser = new Map(); // (userId: number) -> User
    this.idToNotes = new Map(); // (userId: number) -> Note[]
  }

  addUser(user) {
    if (this.getUserByName(user) != null) {
      throw new Error("<marquee>Username already exists</marquee>");
    }
    user.id = crypto.randomBytes(32).toString("base64");
    this.idToUser.set(user.id, user);
    this.idToNotes.set(user.id, []);
    return user;
  }

  getUser(id) {
    return this.idToUser.get(id);
  }

  getUserByName(user) {
    for (const u of this.idToUser.values()) {
      if (u.name == user.name) return u;
    }
    return null;
  }

  addNote(user, note) {
    const notes = this.idToNotes.get(user.id);
    if (notes.length > 50) {
      throw new Error("<marquee>Too many notes</marquee>");
    }
    notes.push(note);
  }

  getNotes(user) {
    return this.idToNotes.get(user.id);
  }
}

module.exports = new Db();
