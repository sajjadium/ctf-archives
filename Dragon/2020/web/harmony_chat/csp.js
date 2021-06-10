"use strict"
const utils = require("./utils")

const REPORT_URL = "/csp-report"
const REPORT_SCHEMA = {
  "type": "object",
  "properties": {
    "csp-report": {
      "type": "object",
      "properties": {
        "blocked-uri": {
          "type": "string"
        },
        "document-uri": {
          "type": "string"
        },
        "effective-directive": {
          "type": "string"
        },
        "original-policy": {
          "type": "string"
        },
        "referrer": {
          "type": "string"
        },
        "status-code": {
          "type": ["integer", "string"]
        },
        "violated-directive": {
          "type": "string"
        }
      },
      "required": [
        "blocked-uri", "document-uri", "effective-directive", "original-policy",
        "referrer", "status-code", "violated-directive"
      ]
    },
  },
  "required": [ "csp-report" ],
  "additionalProperties": false
}

const injectCSPHeaders = (req, res) => {
  const policy = [
    "default-src 'none'",
    "style-src-elem 'self'",
    "style-src 'self'",
    "img-src 'self'",
    "script-src-elem 'self'",
    "script-src 'self'",
    "connect-src 'self'",
    `report-uri ${REPORT_URL}`
  ]

  res.setHeader("Content-Security-Policy", policy.join(";"))
}

const handleReport = (req, res) => {
  let data = Buffer.alloc(0)

  req.on("data", chunk => {
    data = Buffer.concat([data, chunk])
  })

  req.on("end", () => {
    res.status(204).end()

    if (!isLocal(req)) {
      return
    }

    try {
      const report = utils.validateAndDecodeJSON(data, REPORT_SCHEMA)
      console.error(generateTextReport(report["csp-report"]))
    } catch (error) {
      console.warn(error)
      return
    }
  })
}

const generateTextReport = report => {
  let text = "\nContent Security Policy violation!\n"
  text += `Document URI: ${report["document-uri"]}\n`
  text += `Blocked URI : ${report["blocked-uri"]}\n`
  text += `Directive   : ${report["violated-directive"]}\n`
  text += `Full Policy : ${report["original-policy"]}\n`

  if (report["script-sample"]) {
    text += `Sample      : ${report["script-sample"]}\n`
  }

  let sourceInfo = ""
  if (report["source-file"]) {
    sourceInfo += report["source-file"]
  }

  if (report["line-number"]) {
    sourceInfo += `:${report["line-number"]}`
  }

  if (report["column-number"]) {
    sourceInfo += `:${report["column-number"]}`
  }

  if (sourceInfo.length > 0) {
    text += `Source      : ${sourceInfo}\n`
  }

  return text
}

const ContentSecurityPolicy = (req, res, next) => {
  if (req.path === REPORT_URL &&
      req.method === "POST" &&
      req.headers["content-type"] === "application/csp-report") {
    handleReport(req, res)
    return
  }

  injectCSPHeaders(req, res)
  next()
}

const isLocal = (req) => {
  const ip = req.connection.remoteAddress
  return ip === "127.0.0.1" || ip === "::1" || ip === "::ffff:127.0.0.1"
}

module.exports = ContentSecurityPolicy
