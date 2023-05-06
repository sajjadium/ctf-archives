const express = require('express');
const bodyParser = require('body-parser');
const ejs = require('ejs');
const fs = require('fs');
const merge = require('utils-merge');
const morgan = require('morgan')


const utils = require('./utils.js');

const app = express();

const port = process.env.PORT || 8000
const host = process.env.HOST || '0.0.0.0'
const flag = process.env.FLAG || 'LINECTF{this_is_fake}';
const secretKey = '123';
const options = {
    ext: '.ejs',
    filename: 'noname',
}

app.use(bodyParser.json());
app.use(morgan('common'))
app.set('view engine', 'ejs');

const authMiddleware = (req, res, next)=>{
    req.ip = req.headers['x-forwarded-for'] || req.connection.remoteAddress;
    if(!utils.checkPermission(req.params.sandboxPath, req.ip, secretKey)) {
        return res.status(401).send('Permission denied.');
    } else {
        next()
    }
}

app.get('/', (req,res)=>{
    let ip = req.headers['x-forwarded-for'] || req.connection.remoteAddress;
    return res.redirect(utils.generateEndpoint(ip, secretKey));
});

app.get('/:sandboxPath', authMiddleware, (req,res)=>{
    note = req.query.note || 'index';
    return res.render(`sandbox/${req.params.sandboxPath}/${note}`);
});

app.post('/:sandboxPath', authMiddleware, (req, res)=>{
    let saveOptions = {}
    let isChecked = true;
    let path = '';

    merge(saveOptions, options)
    merge(saveOptions, req.body)

    if(saveOptions.filename === undefined || saveOptions.contents === undefined ||
        typeof saveOptions.filename !== 'string' || typeof saveOptions.contents !== 'string') 
        isChecked = false

    if(!saveOptions.ext.includes('.ejs') || saveOptions.ext.length !== 4) isChecked = false;

    if(isChecked) {
        let filename = saveOptions.filename || 'noname';
        filename += saveOptions.ext
        let body = saveOptions.contents;
        if(utils.sanitize(body)){
            let uploadPath = `./views/sandbox/${req.params.sandboxPath}/${filename}`;
            if(!fs.existsSync(uploadPath)){
                fs.writeFile(uploadPath, body, (err)=>{
                    if(err) {
                        console.log(`[!] File write error: ${uploadPath}`);
                        isChecked = false
                    }
                    console.log(`[*] Created ${uploadPath} by ${req.ip} (endpoint: ${req.params.sandboxPath})`);
                });
            } else {
                isChecked = false
            }
        } else {
            isChecked = false
        }
        
    }

    if(isChecked) path = `/${req.params.sandboxPath}/${saveOptions.filename}`;

    let result = {
        result: isChecked,
        path
    };

    return res.json(result)
});

app.get('/:sandboxPath/:filename', authMiddleware, (req,res)=>{
    try {
        res.render(`sandbox/${req.params.sandboxPath}/${req.params.filename}`, {flag});
    } catch {
        res.status(404).send('Not found.');
    }
});

app.listen(port, host, ()=>{
    console.log(`Server running on port ${port}`)
});
