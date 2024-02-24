const uuid = require("uuid");
const fs = require("fs");
const sanitize = require("sanitize-filename");
const crypto=require('crypto');

const users = [];
const notes = [];
const sharedNotes = [];

if (!fs.existsSync("./notes")) fs.mkdirSync("./notes");

function generateNoteId(length) {
  const characters = 'abcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    const randomIndex = crypto.randomInt(characters.length);
    result += characters.charAt(randomIndex);
  }
  return result;
}

const createUser = (username, password) => {
  const user = users.find((u) => u.username === username);
  if (user) {
    return null;
  }
  const id = uuid.v4();
  fs.mkdirSync(`./notes/${id}`);
  users.push({ id, username, password });
  return id;
};

const getUser = (username, password) => {
  const user = users.find(
    (u) => u.username === username && u.password === password
  );
  return user;
};

const createNote = (title, note, owner) => {
  const noteid = generateNoteId(8);
  fs.writeFileSync(`./notes/${owner}/${sanitize(title)}-${noteid}.txt`, note);
  notes.push({ noteid, title, owner });
  return noteid;
};

const getNote = (noteid, owner) => {
  const note = notes.find((n) => n.noteid === noteid && n.owner === owner);
  return note;
};

const deleteNote = (noteid, owner) => {
  const note = getNote(noteid, owner);
  if (note) {
    fs.unlinkSync(`./notes/${owner}/${sanitize(note.title)}-${noteid}.txt`);
    notes.splice(notes.indexOf(note), 1);
  }
};

const shareNote = (noteid, owner) => {
  const note = getNote(noteid, owner);
  sharedNotes.push(note);
  return noteid;
};

const getsharedNote = (noteid) => {
  const note = sharedNotes.find((n) => n.noteid === noteid);
  return note;
};

module.exports = {
  createUser,
  getUser,
  createNote,
  getNote,
  deleteNote,
  shareNote,
  getsharedNote,
};
