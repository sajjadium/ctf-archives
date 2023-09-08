import std/[os, httpcore, json]
import jester

let userDir = getEnv("USER_DIR", "/tmp/users")

proc getUserFilePath(username: string): string =
  let filename = extractFilename(username & ".json")
  return joinPath(userDir, filename)

template errorJSON(msg: string) =
  resp %*{
    "error": msg
  }

routes:
  get "/":
    resp "hello world"

  post "/register":
    let data = parseJSON(request.body)
    if data{"username"} == nil or data{"password"} == nil or data{
        "privilegeLevel"} == nil:
      errorJSON "missing username or password or privilegeLevel"
      return
    let username = data["username"].getStr()
    let password = data["password"].getStr()
    let privilegeLevel = data["privilegeLevel"].getStr()
    if len(username) < 8 or len(password) < 8:
      errorJSON "username and password must be at least 8 characters"
      return
    if privilegeLevel != "user":
      errorJSON "privilegeLevel must be user"
      return
    let jsonFile = getUserFilePath(username)
    if existsFile(jsonFile):
      errorJSON "user already exists"
      return
    let f = open(jsonFile, fmWrite)
    f.write(data)
    f.close()
    resp %*{
      "success": true
    }

  post "/login":
    let data = parseJSON(request.body)
    if data{"username"} == nil or data{"password"} == nil:
      errorJSON "missing username or password"
      return
    let username = data["username"].getStr()
    let password = data["password"].getStr()
    let jsonFile = getUserFilePath(username)
    if not existsFile(jsonFile):
      errorJSON "user does not exist"
      return
    let f = open(jsonFile, fmRead)
    let user = parseJSON(f.readAll())
    f.close()
    if user["password"].getStr() != password:
      errorJSON "incorrect password"
      return
    resp %*{
      "success": true,
      "data": user
    }

  post "/change_password":
    let data = parseJSON(request.body)
    if data{"username"} == nil or data{"old_password"} == nil or data{
        "new_password"} == nil:
      errorJSON "missing username or old_password or new_password"
      return
    let username = data["username"].getStr()
    let oldPassword = data["old_password"].getStr()
    let newPassword = data["new_password"].getStr()
    if len(newPassword) < 8:
      errorJSON "new password must be at least 8 characters"
      return
    let jsonFile = getUserFilePath(username)
    if not existsFile(jsonFile):
      errorJSON "user does not exist"
      return
    let f = open(jsonFile, fmRead)
    let user = parseJSON(f.readAll())
    f.close()
    if user["password"].getStr() != oldPassword:
      errorJSON "incorrect password"
      return
    user["password"].str = newPassword
    let f2 = open(jsonFile, fmWrite)
    f2.write(user)
    f2.close()
    resp %*{
      "success": true
    }
