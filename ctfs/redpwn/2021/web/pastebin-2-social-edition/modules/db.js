class Database {
  constructor() {
    // id -> notes
    this.pastes = new Map();
    // id -> comments
    this.comments = new Map();
  }

  createPaste(id, content) {
    this.pastes.set(id, content);
    this.comments.set(id, []);
  }

  getPaste(id) {
    return this.pastes.get(id);
  }

  createComment(id, comment) {
    this.comments.get(id).push(comment);
  }

  getComments(id) {
    return this.comments.get(id);
  }
}

module.exports = Database;
