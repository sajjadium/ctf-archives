import { createTransport } from "nodemailer";
import * as amqp from "amqplib";
import { Provider } from "nconf";
import MailMessage = require("nodemailer/lib/mailer/mail-message");

const nconf = (new Provider())
    .argv()
    .env()
    .defaults({
        "P_RABBIT_USER": "test",
        "P_RABBIT_PASS": "test",
        "P_RABBIT_HOST": "localhost",
        "P_RABBIT_PORT": "5672",
        "P_SENDGRID_USER": "apikey",
        "P_SENDGRID_PASS": null,
    });

const main = async () => {
    const rabbit = await amqp.connect({
        hostname: nconf.get("P_RABBIT_HOST"),
        port: nconf.get("P_RABBIT_PORT"),
        username: nconf.get("P_RABBIT_USER"),
        password: nconf.get("P_RABBIT_PASS"),
    });

    let transport = createTransport({
        host: "smtp.sendgrid.net",
        port: 465,
        secure: true,
        auth: {
            user: nconf.get("P_SENDGRID_USER"),
            pass: nconf.get("P_SENDGRID_PASS")
        }
    });

    let channel = await rabbit.createChannel();
    channel.consume("email", async (msg) => {
        if (msg === null) {
            return;
        }
        channel.ack(msg);

        try {
            let data = JSON.parse(msg.content.toString());
            await transport.sendMail({
                from: "plaid2020problem@gmail.com",
                subject: "Your Account",
                ...data,
            });
        } catch (e) {
            console.error(e);
        }
    })
}

main();