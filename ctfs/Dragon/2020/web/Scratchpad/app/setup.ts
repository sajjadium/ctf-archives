import * as assert from 'assert';
import * as massive from 'massive';
import utils from './utils';

assert.ok(process.env.ADMIN_PASSWORD, "ADMIN_PASSWORD is not set");
assert.ok(process.env.FLAG, "FLAG is not set");
assert.ok(process.env.DB, "DB is not set");

async function main() {
  const db = await massive(process.env.DB);
  const user = await db.users.insert({name: 'admin', password: utils.hashPassword(process.env.ADMIN_PASSWORD)}).catch(console.log);
  await db.notes.insert({user_id: user.id, title: "Flag", content: process.env.FLAG, favourite: true});
}

main();
