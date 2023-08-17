const { ApolloServer } = require('apollo-server');
const notes = require('./mockData');
const db = require('./db');
const typeDefs = require('./schema');
const resolvers = require('./resolvers');

const server = new ApolloServer({ typeDefs, resolvers, playground: false});

//Pre-populate the db with some notes for demo convinience (not something I would do in real projects)
notes.map(note => db.pushNote(note.id, note));
console.log(`Loaded ${db.getNotes().length} items`);

server.listen().then(({ url }) => {
    console.log(`Api ready at ${url}`);
});
