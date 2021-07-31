import ftpServer from "./ftpServer.js"
import httpServer from "./httpServer.js"

const HTTP_PORT = 1337
const FTP_PORT = 21

const Users = new Map()

httpServer.listen(HTTP_PORT, "0.0.0.0", () => {
    console.log(`HTTP server listening on port ${HTTP_PORT}`)
})

// our ftp server is for internal access ONLY!
ftpServer.listen(FTP_PORT, "127.0.0.1", () => {
    console.log(`FTP server listening on port ${FTP_PORT}`)
})

export { Users }
