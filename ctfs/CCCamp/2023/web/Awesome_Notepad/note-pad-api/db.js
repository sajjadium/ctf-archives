const { JsonDB } = require('node-json-db');
const { Config } = require('node-json-db/dist/lib/JsonDBConfig');

var db = new JsonDB(new Config('notesDB', true, true, '/'));
console.log('Database: notesDB initialized');

module.exports = {
    pushNote: (id, data) => db.push(`/note/${id}`, data),
    getNotes: () => Object.values(db.getData('/note')),
    deleteNote: id => db.delete(`/note/${id}`),
    pushTicket: (id, data) => db.push(`/ticket/${id}`, data),
    getTickets: () => Object.values(db.getData('/ticket')),
    deleteTicket: id => db.delete(`/ticket/${id}`)
};
