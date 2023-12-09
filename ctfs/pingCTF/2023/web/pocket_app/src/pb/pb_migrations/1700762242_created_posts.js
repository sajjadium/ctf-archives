/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const collection = new Collection({
    "id": "b7ioytdo5ryd244",
    "created": "2023-11-23 17:57:22.020Z",
    "updated": "2023-11-23 17:57:22.020Z",
    "name": "posts",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "8f7ocaie",
        "name": "user",
        "type": "relation",
        "required": true,
        "presentable": false,
        "unique": false,
        "options": {
          "collectionId": "_pb_users_auth_",
          "cascadeDelete": true,
          "minSelect": null,
          "maxSelect": 1,
          "displayFields": null
        }
      },
      {
        "system": false,
        "id": "ypejix9p",
        "name": "content",
        "type": "editor",
        "required": true,
        "presentable": false,
        "unique": false,
        "options": {
          "convertUrls": false
        }
      }
    ],
    "indexes": [],
    "listRule": "@request.auth.id = user.id",
    "viewRule": "@request.auth.id = user.id || @request.auth.isModerator = true",
    "createRule": "",
    "updateRule": "@request.auth.id = user.id",
    "deleteRule": "@request.auth.id = user.id",
    "options": {}
  });

  return Dao(db).saveCollection(collection);
}, (db) => {
  const dao = new Dao(db);
  const collection = dao.findCollectionByNameOrId("b7ioytdo5ryd244");

  return dao.deleteCollection(collection);
})
