var rootUser = process.env.MONGO_INITDB_ROOT_USERNAME;
var rootPassword = process.env.MONGO_INITDB_ROOT_PASSWORD;
var admin = db.getSiblingDB('admin');
admin.auth(rootUser, rootPassword);
var user = process.env.MONGO_INITDB_USERNAME
var password = process.env.MONGO_INITDB_PASSWORD;
db.createUser({ user: user, pwd: password, roles: ["readWrite"] });
