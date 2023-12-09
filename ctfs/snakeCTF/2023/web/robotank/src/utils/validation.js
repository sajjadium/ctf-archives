const { validationResult, matchedData } = require("express-validator");
const { validate: uuidValidate, version: uuidVersion } = require("uuid");

const validate = (req, res) => {
  const result = validationResult(req);
  if (result.isEmpty()) {
    return matchedData(req);
  } else {
    res.status(400).json({ result: "failure", message: "Invalid request" });
    return null;
  }
};

const isUuid = (uuid) => {
  return uuidValidate(uuid) && uuidVersion(uuid) === 4;
};

module.exports = { validate, isUuid };
