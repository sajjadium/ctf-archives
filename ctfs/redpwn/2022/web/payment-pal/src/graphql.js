const { graphqlHTTP } = require('express-graphql');
const { buildSchema } = require('graphql');
const crypto = require("crypto");

const db = require("./db.js");
const auth = require("./auth.js");

const sha256 = (data) => crypto.createHash('sha256').update(data).digest('hex');

// Construct a schema, using GraphQL schema language
const schema = buildSchema(`
type Query {
  info: User,
  flag: String
}

type Mutation {
  login(username: String!, password: String!): User
  register(username: String!, password: String!): User
  transfer(recipient: String!, amount: Int!): User
  addContact(username: String!): User
  logout: Boolean
}

type User {
  username: String!
  money: Int!
  isAdmin: Boolean!
  contacts: [String]
}
`);

// queries

const info = (_, { req }) => {
  return { ...auth.getUser(req), password: null };
};

const flag = (_, { req }) => {
  const user = auth.getUser(req);
  if(user.username.startsWith("admin-")) {
    throw new Error("no");
  }
  if(user.money <= 0x12345) {
    throw new Error("poor");
  }
  return process.env.FLAG || "hope{test_flag}";
};

// mutations

const login = ({ username, password }, { res }, context) => {
  let user = db.getUser(username);
  if(!user) {
    throw new Error("Username or password invalid");
  }

  if(user.password !== sha256(password)) {
    throw new Error("Username or password invalid");
  }

  auth.setUser(res, username);
  return { ...user, password: null };
};

const register = ({ username, password }, { res }, context) => {
  if(db.getUser(username)) {
    throw new Error("A user already exists with that username");
  }

  if(username.length < 5 || password.length < 8) {
    throw new Error("Use something more secure");
  }

  let user = {
    username,
    password: sha256(password),
    money: 0,
    isAdmin: false
  };
  db.setUser(username, user);

  auth.setUser(res, username);
  return { ...user, password: null };
};

const transfer = ({ recipient, amount }, { req }) => {
  const user = auth.getUser(req);

  if(amount <= 0) {
    throw new Error("Amount must be positive");
  }

  if(amount > user.money) {
    throw new Error("You do not have enough money for this transfer");
  }

  recipient = db.getUser(recipient);
  if(!recipient) {
    throw new Error("No recipient exists with that username");
  }
  user.money -= amount;
  recipient.money += amount;

  return { ...user, password: null };
};

const logout = (_, { res }) => {
  res.clearCookie("session");
  return true;
};

// WIP feature...
const addContact = ({ username }, { req }) => {
  const user = auth.getUser(req);

  if(!user.contacts) user.contacts = [];
  user.contacts.push(username);

  return { ...user, password: null };
};

const root = {
  // queries
  info,
  flag,
  // mutations
  login,
  register,
  transfer,
  logout,
  addContact
};

module.exports = graphqlHTTP(async (req, res) => ({
  schema: schema,
  rootValue: root,
  graphiql: false,
  context: { req, res }
}));