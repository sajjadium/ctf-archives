const db = require('./db');

const resolvers = {
    Query: {
        notes: () => {
            try {
                return db.getNotes();
            } catch (error) {
                console.log('error in query Notes:', error);
                return { status: '500', message: 'error' };
            }
        },
        tickets: () => {
            try {
                return db.getTickets();
            } catch (error) {
                console.log('error in query Tickets:', error);
                return { status: '500', message: 'error' };
            }
        }
    },
    Mutation: {
        addNote: (parent, args) => {
            try {
                const id = require('crypto')
                    .randomBytes(10)
                    .toString('hex');
                const note = {
                    id,
                    title: args.title,
                    body: args.body
                };
                db.pushNote(id, note);
                console.log(`added note id:${id}`);

                return note;
            } catch (error) {
                console.log('error in addNote:', error);
                return { status: '500', message: 'error' };
            }
        },
        saveNote: (parent, args) => {
            try {
                const note = {
                    id: args.id,
                    title: args.title,
                    body: args.body
                };
                db.pushNote(note.id, note);
                console.log(`saved note id:${note.id}`);
                return note;
            } catch (error) {
                console.log('error in saveNote:', error);
                return { status: '500', message: 'error' };
            }
        },
        deleteNote: (parent, args) => {
            try {
                db.deleteNote(args.id);
                console.log(`deleted note id:${args.id}`);
                return { status: '200', message: 'ok' };
            } catch (error) {
                console.log('error in deleteNote:', error);
                return { status: '500', message: 'error' };
            }
        },
        addTicket: (parent, args) => {
            try {
                const id = require('crypto')
                    .randomBytes(10)
                    .toString('hex');
                const ticket = {
                    id,
                    issue: rep(args.issue),
                };
                db.pushTicket(id, ticket);
                console.log(`added ticket id:${id}`);

                return ticket;
            } catch (error) {
                console.log('error in addTicket:', error);
                return { status: '500', message: 'error' };
            }
        },
        saveTicket: (parent, args) => {
            try {
                const ticket = {
                    id: args.id,
                    issue: args.issue,
                };
                db.pushTicket(ticket.id, ticket);
                console.log(`saved ticket id:${ticket.id}`);
                return ticket;
            } catch (error) {
                console.log('error in saveNote:', error);
                return { status: '500', message: 'error' };
            }
        },
        deleteTicket: (parent, args) => {
            try {
                db.deleteTicket(args.id);
                console.log(`deleted ticket id:${args.id}`);
                return { status: '200', message: 'ok' };
            } catch (error) {
                console.log('error in deleteTicket:', error);
                return { status: '500', message: 'error' };
            }
        }
    }
};

function rep(text) {
    return text.replace(/&/g, '&amp;').
      replace(/</g, '&lt;').
      replace(/"/g, '&quot;').
      replace(/'/g, '&#039;');
 }

module.exports = resolvers;
