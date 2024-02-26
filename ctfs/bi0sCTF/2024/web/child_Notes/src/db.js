const { Model } = require("objection");
const Knex = require("knex");

const knex = Knex({
  client: "sqlite3",
  connection: {
    filename: "./database.xlsx",
  },
  useNullAsDefault: true,
});

Model.knex(knex);

module.exports = knex;
