import std/asynchttpserver
import std/asyncdispatch
import std/db_sqlite
import std/strutils
import std/strformat
import std/sequtils
import std/options
import std/sysrand
import std/cookies
import std/strtabs
import std/json
import std/uri
import tables
import os

proc loadResources(): Table[string, string] =
  var resources = initTable[string, string]()

  for file in walkDirRec("./resources", yieldFilter = {pcFile}):
    resources[file] = readFile(file)

  for file in walkDirRec("./views", yieldFilter = {pcFile}):
      resources[file] = readFile(file)

  return resources

proc randId(): string =
  const hexChars = "0123456789abcdef"
  let n = urandom(32)
  result = newStringOfCap(64)

  for b in n:
    result.add(hexChars[int(b shr 4 and 0x0f'u8)])
    result.add(hexChars[int(b and 0x0f'u8)])

func parseBody(body: string): Option[Table[string, string]] =
  var parsed = initTable[string, string]()

  try:
    for param in body.split("&"):
      let split = param.split("=", 2)
      parsed[split[0]] = decodeUrl(split[1])

    return some(parsed)
  except CatchableError:
    return none(Table[string, string])

func headersFromFile(name: string): array[0..0, (string, string)] =
  if name.endsWith("js"):
    return {"Content-type": "application/javascript; charset=utf-8"}

  if name.endsWith("css"):
    return {"Content-type": "text/css; charset=utf-8"}

  if name.endsWith("html"):
    return {"Content-type": "text/html; charset=utf-8"}

  return {"Content-type": "text/plain; charset=utf-8"}

func idsFromRequest(req: Request): seq[string] =
  if req.headers.table.contains("cookie"):
    let cookie = parseCookies(req.headers.table["cookie"][0])
    result = cookie.getOrDefault("notes", "").split(",")
  else:
    result = @[""]

const resources = loadResources()

proc main {.async.} =
  let db = open("/data/notes.sqlite", "", "", "")

  var server = newAsyncHttpServer()

  proc not_found(req: Request) {.async.} =
    await req.respond(Http404, "resource not found", headersFromFile("plain").newHttpHeaders())

  proc err_resp(req: Request) {.async.} =
    await req.respond(Http500, "Unkonwn error", headersFromFile("plain").newHttpHeaders())

  proc handle_resource(req: Request, url: string) {.async.} =
    if resources.hasKey(url):
      await req.respond(Http200, resources[url], headersFromFile(url).newHttpHeaders())
    else:
      await nO_tFo_Und(req)

  proc render_show(id: string): string  =
    let entry = db.getValue(sql"select value from notes where uuid=?", id)
    
    if entry != "":
      return resources["views/show.html"].replace("<!-- NOTE CONTENT -->", entry)
    
    return ""

  proc handle_request(req: Request, url: string) {.async.} =
    case url:
      of "":
        await req.respond(Http200, resources["views/index.html"], headersFromFile("html").newHttpHeaders())
      of "create":
        if req.reqMethod == HttpGet:
          await req.respond(Http200, resources["views/create.html"], headersFromFile("html").newHttpHeaders())
          return

        let body = parseBody(req.body).get(initTable[string, string]())

        if "content" notin body:
          await req.err_resp()
          return

        let id = randId()
        db.exec(sql"insert into notes (uuid, value, created_at) values (?, ?, datetime())", id, body["content"])

        var ids = idsFromRequest(req)
        ids.add(id)

        let newHeader = setCookie("notes", ids.join(","), noName=true)

        var headers = headersFromFile("html").newHttpHeaders()
        headers.add("set-cookie", newHeader)
        headers.add("hx-push", fmt"/show/{id}")

        await req.respond(Http200, render_show(id), headers)
      of "list":
        let ids = %* idsFromRequest(req)

        let values = db.getAllRows(sql"select uuid, value from notes where uuid in (select value from json_each(?)) order by created_at desc", ids)
          .map(proc(r: seq[string]): string = fmt"<section><h3><a href='/show/{r[0]}'>Note</a></h3><p>{r[1]}</p></section>")
          .join("\n")

        await req.respond(Http200, resources["views/list.html"].replace("<!-- LIST -->", values), headersFromFile("html").newHttpHeaders())
      else:
        let fragments = url.split("/")

        if fragments.len != 2 or req.reqMethod != HttpGet:
          await req.not_found()
          return

        let body = render_show(fragments[1])

        if body == "":
          await req.not_found()
        else:
          await req.respond(Http200, body, headersFromFile("html").newHttpHeaders())

  proc cb(req: Request) {.async.} =
    var url = $req.url.path
    removePrefix(url, "/")

    if url.startsWith("resources"):
      await handle_resource(req, url)
    else:
      await req.handle_request(url)

  server.listen(Port(8081))
  while true:
    if server.shouldAcceptRequest():
      await server.acceptRequest(cb)
    else:
      # too many concurrent connections, `maxFDs` exceeded
      # wait 500ms for FDs to be closed
      await sleepAsync(500)

waitFor main()
