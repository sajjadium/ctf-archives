const fs = require('fs')
const escape = require('escape-html')
const exec = require('child_process')

const express = require("express")
const app = express()
app.use(express.static('public'))

const config = JSON.parse(fs.readFileSync('config.json'))
process.env.FLAG = config.flag

const validateRequest = (req) => {
    const url = req.query.url
    if (!url) {
        return 'Hmmm, not seeing a URL. Please try again.'
    }

    let parsedURL
    try {
        parsedURL = new URL(url)
    }
    catch (e) {
        return 'Something is wrong with your url: ' + escape(e.message)
    }

    if (parsedURL.protocol !== 'http:' && parsedURL.protocol !== 'https:') {
        return 'Our admin is picky. Please provide a url with the http or https protocol.'
    }

    if (parsedURL.hostname !== req.hostname) {
        return `Please provide a url with a hostname of: ${escape(req.hostname)}  Hmmm, I guess that will restrict the submissions. TODO: Remove this restriction before the admin notices and we all get fired.`
    }

    return null
}

app.get('/visit', function(req, res) {
    const validateError = validateRequest(req)
    if (validateError) {
        res.send(validateError)
        return
    }

    const file = 'node'
    const args = ['bot.js', config.httpOnly, req.hostname, req.query.url]
    const options = { timeout: 10000 }
    const callback = function(error, stdout, stderr) {
         console.log(error, stdout, stderr);
         res.send('admin bot has visited your url')
     }

    exec.execFile(file, args, options, callback)
});

// useful for debugging cloud deployments
app.get('/debug', function(req, res) {
    if (config.allowDebug) {
        res.send({"remote-ip": req.socket.remoteAddress, ...req.headers})
    }
    else {
        res.send('sorry, debug endpoint is not enabled')
    }
})

app.get('/zombie', function(req, res) {
    const show = req.query.show
    if (!show) {
        res.send('Hmmmm, you did not mention a show')
        return
    }

    const rating = Math.floor(Math.random() * 3)
    let blurb
    switch (rating) {
        case 2:
            blurb = `Wow, we really liked ${show} too!`
            break;
        case 1:
            blurb = `Yeah, ${show} was ok... I guess.`
            break;
        case 0:
            blurb = `Sorry, ${show} was horrible.`
            break;
    }
    res.send(blurb)
})

const port = 80
app.listen(port,() => {
    console.log(`Running on ${port}`);
});