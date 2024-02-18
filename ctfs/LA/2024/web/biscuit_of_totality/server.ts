import { Sha512 } from "https://deno.land/x/sha2@1.0.0/mod/sha512.ts"
import { encodeBase64 } from "https://deno.land/std@0.213.0/encoding/base64.ts"
import { serveDir } from "https://deno.land/std@0.213.0/http/file_server.ts"

const scriptHash = encodeBase64(new Sha512().hashToBytes(await Deno.readFile("./static/index.js")))
const styleHash = encodeBase64(new Sha512().hashToBytes(await Deno.readFile("./static/index.css")))
const indexHtml = (await Deno.readTextFile("./static/index.html"))
  .replace("$SCRIPT_INTEGRITY", scriptHash)
  .replace("$STYLE_INTEGRITY", styleHash)
const headers = {
  "content-security-policy": `default-src 'none'; script-src 'sha512-${scriptHash}'; style-src 'self'; img-src *; form-action 'none'; require-trusted-types-for 'script'; trusted-types 'none'`,
  "x-content-type-options": "nosniff",
  "cache-control": "max-age=86400",
}
const flattenedHeaders = Object.entries(headers).map(([key, value]) => `${key}: ${value}`)

Deno.serve({ port: 8080 }, async req => {
  const path = decodeURIComponent(new URL(req.url).pathname)
  
  if (["/", "/viewSave"].includes(path)) {
    return new Response(indexHtml, {
      headers: {
        ...headers,
        "content-type": "text/html"
      }
    })
  }

  return serveDir(req, {
    fsRoot: "./static",
    headers: flattenedHeaders
  })
})
