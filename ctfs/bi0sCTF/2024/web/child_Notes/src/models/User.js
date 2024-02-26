const { Model } = require("objection");

class User extends Model {
  static get tableName() {
    return "users";
  }
}

module.exports = User;
