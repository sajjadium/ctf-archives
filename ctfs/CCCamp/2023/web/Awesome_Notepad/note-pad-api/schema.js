const { gql } = require('apollo-server');

const typeDefs = gql`
    type Note {
        title: String
        body: String
        id: String
    }

    type Query {
        notes: [Note]
        tickets: [Ticket]
    }

    input NoteInput {
        title: String
        body: String
    }

    type Message {
        status: String
        message: String
    }

    input TicketInput {
        issue: String
    }

    type Ticket {
        id: String
        issue: String
    }

    type Mutation {
        saveNote(id: String, title: String, body: String): Note
        addNote(title: String, body: String): Note
        deleteNote(id: String): Message
        addTicket(issue: String): Ticket
        saveTicket(id: String, issue: String): Ticket
        deleteTicket(id: String): Message
    }
`;

module.exports = typeDefs;
