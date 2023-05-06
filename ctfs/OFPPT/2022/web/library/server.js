const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
    console.log(`Listening on port ${PORT}`);
});

app.get('/getFile', (req, res) => {
    let { file } = req.query;

    if (!file) {
        res.send(`file=${file}\nFilename not specified!`);
        return;
    }

    try {

        if (file.includes(' ') || file.includes('/')) {
            res.send(`file=${file}\nInvalid filename!`);
            return;
        }
    } catch (err) {
        res.send('An error occured!');
        return;
    }

    if (!allowedFileType(file)) {
        res.send(`File type not allowed`);
        return;
    }

    if (file.length > 5) {
        file = file.slice(0, 5);
    }

    const returnedFile = path.resolve(__dirname + '/' + file);

    fs.readFile(returnedFile, (err) => {
        if (err) {
            if (err.code != 'ENOENT') console.log(err);
            res.send('An error occured!');
            return;
        }

        res.sendFile(returnedFile);
    });
});

app.get('/*', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

function allowedFileType(file) {
    const format = file.slice(file.indexOf('.') + 1);

    if (format == 'js' || format == 'ts' || format == 'c' || format == 'cpp') {
        return true;
    }

    return false;
}