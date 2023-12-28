/// <reference path="../node_modules/njs-types/ngx_http_js_module.d.ts" />
import xml from "xml";
import fs from "fs";

/**
 * @typedef {Object} Spaghetti
 * @property {string} name - The name of the recipe.
 * @property {string} recipe - The recipe itself.
 * @property {number} image - The image identifier.
 * @property {number} counter - The counter.
 * @property {Record<string, string>} ingredient - The ingredients of the recipe.
 */


/**
 * @param {Object} schema
 * @param {XMLNode} root
 */
function nodeToJson(schema, root) {
  root.$tags.forEach((node) => {
    if (node.$name in schema) {
      const typename = typeof schema[node.$name];
      if (typename === "string") {
        schema[node.$name] = node.$text;
      } else if (typename === "number") {
        schema[node.$name] = Number(node.$text);
      } else if (typename === "object") {
        const name = node.$tag$name.$text;
        const quantity = node.$tag$quantity.$text;
        Object.assign(schema[node.$name], { [name]: quantity });
      }
    }
  });
}

/**
 * 
 * @param {string} filename 
 * @returns {Spaghetti}
 */

function jsonSpaghetti(filename) {
  const schema = {
    name: "",
    recipe: "",
    image: 0,
    counter: 0,
    ingredient: {},
  };

  const content = fs.readFileSync(filename);
  const doc = xml.parse(content);
  nodeToJson(schema, doc.spaghetti);
  return schema;
}

/**
 *
 * @param {NginxHTTPRequest} r
 */
async function handler(r) {
  const id = r.args.id;
  const filename = `/tmp/${id}`;

  if (!fs.statSync(filename, { throwIfNoEntry: false })) {
    return r.return(404, "Not found");
  }
  const spaghetti = jsonSpaghetti(filename);

  const charset = r.headersIn["Accept-Charset"] ?? "utf-8";
  r.headersOut["Content-Type"] = `application/json; charset=${charset}`;
  return r.return(200, JSON.stringify(spaghetti));
}

export default { handler };