import cors from "@/server/middleware/cors";
import connectDb from "@/server/middleware/mongoose";
import verifyUser from "@/server/middleware/verifyUser";
const net = require('net');

const CHALL_DOMAIN = process.env.CHALL_DOMAIN || 'http://web-noteninja:1337';
const XSSBOT_DOMAIN = process.env.XSSBOT_DOMAIN || 'noteninja-xssbot';
const XSSBOT_PORT = process.env.XSSBOT_PORT || 1337;

const handler = async (req, res) => {
    await res.status(200).json({ message: "Reported to admin successfully!" })

    const url = `${CHALL_DOMAIN}/notes/${req.body.id}`
    const client = net.Socket();
    client.connect(XSSBOT_PORT, XSSBOT_DOMAIN);
    await new Promise(resolve => {
      client.on('data', data => {
        let msg = data.toString();
        if (msg.includes("Please send me")) {
          client.write(url + '\n');
          console.log(`sending to bot: ${url}`);
        }else{
          res.write(msg + '\n')
          if(msg.includes('Page: ')){
            res.write('Done.\n')
            res.end();
          }
        }
      });
    });

};

export default cors(verifyUser(connectDb(handler)));
