const express = require('express')
const http = require('http')
const { spawn } = require('child_process');

const app = express()
app.use(express.urlencoded({ extended: true }))
app.use(express.json())

/**
 *
 * @param {string} url
 * @returns
 */
const curl = (url) => {
    return new Promise((resolve, reject) => {
        if (url.startsWith("gopher") || url.includes("-K")){
            reject(new Error("Error"))
        }
        const proc = spawn('curl', [url]);
        let output = '';

        proc.stdout.on('data', (data) => {
            output += data.toString();
        });

        proc.on('exit', (code) => {
            if (code === 0) {
                resolve(output);
            } else {
                reject(new Error(`Command failed with code ${code}`));
            }
        });
    });
};

/**
 *
 * @param {string} url
 * @param {string} filename
 * @returns
 */
const ftp = (url, filename) => {
    return new Promise((resolve, reject) => {
        const protocol = (new URL(url)).protocol
        if (!(protocol === "ftp:")) {
            return reject(new Error(`Protocol not supported`))
        }
        const proc = spawn('curl', [url, '-o', filename]);
        let output = '';
        proc.stdout.on('data', (data) => {
            output += data.toString();
        });
        proc.on('exit', (code) => {
            if (code === 0) {
                return resolve(output);
            } else {
                return reject(new Error(`Command failed with code ${code}`));
            }
        });
    });
};

app.all("/curl", async (req, res) => {
    const { url } = Object.assign(req.body, req.query)
    if (!url) {
        return res.status(400).send({ "message": "missing url" })
    }
    return curl(url).then(data => {
        return res.send({ "message": data })
    }).catch(e => {
        return res.status(500).send({ "message": e.toString() })
    })
})

app.all("/ftp", async (req, res) => {
    const { url, filename } = Object.assign(req.body, req.query)
    if (!url || !filename) {
        return res.status(400).send({ "message": "missing url or filename" })
    }
    return ftp(url, filename).then(data => {
        return res.send({ "message": data })
    }).catch(e => {
        return res.status(500).send({ "message": e.toString() })
    })
})

http.createServer(app).listen(5000, "0.0.0.0")
