"use strict"
const Ajv = require("ajv")
const ajv = new Ajv({
  strictDefaults: true,
  strictKeywords: true,
  strictNumbers: true
})

const crypto = require("crypto")
const json = require("javascript-serializer")

const utils = {}

utils.validateAndDecodeJSON = (data, jsonSchema) => {
  const decoded = JSON.parse(data)

  const result = ajv.validate(jsonSchema, decoded)
  if (!result) {
    throw ajv.errorsText()
  }

  return json.fromJSON(decoded)
}

utils.generateNewId = () => {
  const id = Buffer.alloc(16)
  return crypto.randomFillSync(id).toString("hex")
}

module.exports = utils
