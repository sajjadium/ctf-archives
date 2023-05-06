import ftpd from "ftpd"

import { Users } from "./index.js"
import UserFS from "./userfs.js"

const server = new ftpd.FtpServer("127.0.0.1", {
    getInitialCwd: _conn => "/",
    getRoot: _conn => "/",
    useWriteFile: true,
    useReadFile: true,
    maxStatsAtOnce: 1,
})

server.on("error", error => {
    console.log(`FTP error: ${error}`)
})

server.on("client:connected", conn => {
    conn._command_PASV = () => {conn.respond("502 PASV mode disabled")}
    let user = null

    conn.on("command:user", (username, succeed, fail) => {
        console.log(`attempt user: ${username}`)

        const candidateUser = Users.get(username)
        if (!candidateUser) {
           fail()
           return
        }

        user = candidateUser
        succeed()
    })

    conn.on("command:pass", (pass, succeed, fail) => {
        console.log(`FTP login: ${user.username}:${pass}`)
        if (user.password === pass) {
            console.log("successful login")
            succeed(user.username, new UserFS(user))
        }
        else {
            fail()
        }
    })
})

server.debugging = 4
export default server
