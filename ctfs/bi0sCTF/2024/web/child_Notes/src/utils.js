const crypto = require("crypto");
const uuid = require("uuid");
const User = require("./models/User");
const Post = require("./models/Post");
const knex = require("./db");

const TEMPLATE = "./public/template.html";

const init = async (admin_pass) => {
  await knex.schema.dropTableIfExists("users");
  await knex.schema.dropTableIfExists("posts");

  await knex.schema.createTable("users", (table) => {
    table.increments("id").primary();
    table.string("username");
    table.string("password");
  });

  await knex.schema.createTable("posts", (table) => {
    table.uuid("id").primary();
    table.string("title");
    table.string("content");
    table.string("author");
  });

  //For security reasons, LOL
  for (let i = 0; i < 10; i++) {
    const username = "admin" + crypto.randomBytes(16).toString("hex");
    await User.query().insert({
      username,
      password: crypto.randomBytes(16).toString("hex"),
    });
    await Post.query().insert({
      id: uuid.v4(),
      title: crypto.randomBytes(16).toString("hex"),
      content: crypto.randomBytes(100).toString("hex"),
      author: username,
    });
  }

  await User.query().insert({ username: "admin", password: admin_pass });
  await Post.query().insert({
    id: uuid.v4(),
    title: process.env.FLAG || "bi0sctf{fake_flag}",
    content: require("fs").readFileSync(TEMPLATE).toString(),
    author: "admin",
  });

  console.log("Initiated with Password: " + admin_pass);
};

module.exports = { init };
