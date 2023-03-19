const zombie = require("zombie")

const browser = new zombie ({
    waitDuration: 5*1000,
    localAddress: 0 // without this, calls to localhost fail!
})

const httpOnly = process.argv[2] === 'true'
const hostname = process.argv[3]
const url = process.argv[4]

browser.setCookie({ name: 'flag', domain: hostname, path:'/', value: process.env.FLAG, httpOnly: httpOnly})

browser.visit(url, function() {
    console.log("Visited: ", url)
})    
