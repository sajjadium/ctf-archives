const express = require("express");
const { graphqlHTTP } = require("express-graphql");
const {
  GraphQLObjectType,
  GraphQLSchema,
  GraphQLID,
  GraphQLString,
  GraphQLList,
} = require("graphql");
const rateLimit = require("express-rate-limit");
const depthLimit = require("graphql-depth-limit");
const path = require("path");

const app = express();
const limiter = rateLimit({ windowMs: 60 * 1000, max: 10 });
app.use(limiter);
app.use(express.static(path.join(__dirname, "public")));

const users = [
  { id: "1", name: "Monica", friends: ["2", "3"] },  //other fields may exist
  { id: "2", name: "Rachel", friends: ["4"] },
  { id: "3", name: "Ross", friends: ["5"] },
  { id: "4", name: "Phoebe", friends: ["6"] },
  { id: "5", name: "Joey", friends: ["6"] },
  { id: "6", name: "Chandler", friends: [] }
];

const getUserById = (id) => users.find((u) => u.id === id);

const noIntrospectionRule = (context) => ({
  Field(node) {
    if (node.name.value === "__schema" || node.name.value === "__type") {
      throw new Error("Introspection is disabled");
    }
  },
});

const UserType = new GraphQLObjectType({
  name: "User",
  fields: () => ({
    id: { type: GraphQLID },
    name: { type: GraphQLString },
    friends: {
      type: GraphQLList(UserType),
      resolve: (user, args, context) => {
        context.traversedFromFriendChain = true;
        return user.friends.map(getUserById);
      },
    }
    // other fields may exist...
  }),
});

const QueryType = new GraphQLObjectType({
  name: "Query",
  fields: {
    me: { type: UserType, resolve: () => getUserById("1") },
    user: {
      type: UserType,
      args: { id: { type: GraphQLID } },
      resolve: (_, { id }) => getUserById(id),
    },
  },
});

const schema = new GraphQLSchema({ query: QueryType });

app.use(
  "/graphql",
  graphqlHTTP((req) => ({
    schema,
    graphiql: true,
    validationRules: [depthLimit(3), noIntrospectionRule],
    context: {},
  }))
);

app.listen(1337, () => console.log("App running on port 1337"));
