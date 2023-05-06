import * as express from "express";
import * as jwt from "express-jwt";
import * as crypto from "crypto";
import { Request, Response } from "express";
import { getConnection } from "typeorm";
import { User } from "../entity/User";
import * as moment from "moment";
import { createClient } from 'redis';
const client = createClient();
client.connect();


const data = require('../../projectconfig.json');
let router = express.Router();
const secret = data["jwt-secret"];


router.get("/users/", jwt({ secret: secret, algorithms: ['HS256'] }), async function (req: any, res: Response) {
    const conn = getConnection();
    const userRepository = conn.getRepository(User);
    const results = await userRepository.findOne(req.user.id);
    return res.send(results);
});

router.put("/users/", jwt({ secret: secret, algorithms: ['HS256'] }), async function (req: any, res: Response) {
    const conn = getConnection();
    const userRepository = conn.getRepository(User);
    const user = await userRepository.findOne(req.user.id);
    userRepository.merge(user, req.body);
    const results = await userRepository.save(user);
    return res.send(results);
});

router.post("/images/", jwt({ secret: secret, algorithms: ['HS256'] }), async function (req: any, res: Response) {
    const conn = getConnection();
    const userRepository = conn.getRepository(User);
    const user = await userRepository.findOne(req.user.id);
    const hash = crypto.createHash('sha256');
    hash.update(moment().format());
    const filename = hash.digest('hex');
    console.log(req.files);
    
    if (req.files && req.files.image) {
        let image = req.files.image;
        let uploadPath = __dirname + '/../images/' + filename + '.jpg';
        image.mv(uploadPath, async function(err) {
            if (err)
              return res.status(500).send(err);
            userRepository.merge(user, { images: user.images + filename +'.jpg,' });
            const results = await userRepository.save(user);
            res.send('File uploaded!');
        });
    }
});

router.get("/images/", jwt({ secret: secret, algorithms: ['HS256'] }), async function (req: any, res: Response) {
    const conn = getConnection();
    const userRepository = conn.getRepository(User);
    const user = await userRepository.findOne(req.user.id);
    const images = user.images.split(',');
    images.pop();
    return res.send(images);
});

router.post("/report/", jwt({ secret: secret, algorithms: ['HS256'] }), async function (req: any, res: Response) {
    console.log(req.body);
    await client.lPush("submissions",req.body.url).then(()=>{
        return res.send("Reported");
    });
});

export = router