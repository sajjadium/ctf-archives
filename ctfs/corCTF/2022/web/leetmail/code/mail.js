import { SMTPServer } from 'smtp-server'
import { simpleParser } from 'mailparser'
import { addEmail } from './db.js'

const readMax = async (stream, n) => {
    let total = 0
    const chunks = []

    for await (const chunk of stream) {
        total += chunk.length
        chunks.push(chunk)
        if (total > n) {
            return;
        }
    }

    return Buffer.concat(chunks);
}

async function readMail(stream, session, callback) {
    const data = await readMax(stream, 200 * 1024);
    if (!data) {
        let err = new Error('Message too large');
        err.responseCode = 552;
        return callback(err);
    }

    const parsed = await simpleParser(data, {
        skipImageLinks: true
    });

    if (parsed.from.value.length > 10) {
        let err = new Error('Too many recipients');
        err.responseCode = 452;
        return callback(err);
    }

    for (let recipient of parsed.to.value) {
        console.log('Sending email to', recipient.address.toLowerCase());
        try {
            addEmail(recipient.address.toLowerCase(), data.toString());
        } catch(e) {
            let err = new Error('Recipient not found');
            err.responseCode = 550;
            return callback(err);
        }
    }

    callback(null, 'Message saved.')
}


export default () =>  {
    const server = new SMTPServer({
        authOptional: true,
        onData: readMail,
        logger: true,
        disabledCommands: ['STARTTLS']
    });

    server.listen(25);
}