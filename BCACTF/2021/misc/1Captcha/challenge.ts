import { NextApiRequest, NextApiResponse } from 'next';
import { CompactEncrypt } from 'jose/jwe/compact/encrypt';
import { compactDecrypt } from 'jose/jwe/compact/decrypt';
import { createCanvas, loadImage } from 'canvas';
import randomColor from 'randomcolor';

const challengeKey = Buffer.from(process.env.CAPTCHA_CHALLENGE_KEY!, "hex");
const encoder = new TextEncoder();
const decoder = new TextDecoder();
const stages = 20;

interface Challenge {
    stage: number;
    expected: boolean;
    correct: boolean[];
    expires: number;
}

function randomBool(): boolean {
    return Math.random() > 0.5;
}

function timeLimit(stage: number) {
    if (stage === 0) return 120;
    if (stage === 1) return 30;
    return Math.min(Math.max(2, 13 - stage), 10);
}

const image1 = loadImage("1.png");
const imagel = loadImage("l.png");

async function generateImage(input: boolean): Promise<string> {
    const canvas = createCanvas(64, 64);
    const ctx = canvas.getContext("2d");
    const lightBackground = randomBool();
    ctx.fillStyle = randomColor({luminosity: lightBackground ? "light" : "dark"});
    ctx.fillRect(0, 0, 64, 64);
    ctx.globalCompositeOperation = "destination-out";
    ctx.drawImage(input ? (await image1) : (await imagel), Math.floor(Math.random() * 48), Math.floor(Math.random() * 32));
    ctx.globalCompositeOperation = "destination-over";
    ctx.fillStyle = randomColor({luminosity: lightBackground ? "dark" : "light"});
    ctx.fillRect(0, 0, 64, 64);
    return canvas.toDataURL();
}

export default async (req: NextApiRequest, res: NextApiResponse) => {
    let stage = 0;
    if (typeof req.headers["x-captcha-challenge"] === "string") {
        let challenge: Challenge;
        try {
            const {plaintext} = await compactDecrypt(req.headers["x-captcha-challenge"], challengeKey);
            challenge = JSON.parse(decoder.decode(plaintext));
        } catch (e) {
            res.status(400);
            res.json({error: "Unable to parse challenge token"});
            return;
        }

        if (challenge.expires < Date.now() / 1000) {
            res.status(400);
            res.json({error: "Challenge expired"});
            return;
        }
        
        const answer: unknown = req.body.answer;
        if (typeof answer !== "object" || !(answer instanceof Array)) {
            res.status(400);
            res.json({error: "answer must be an array"});
            return;
        }
        if (answer.length !== 9) {
            res.status(400);
            res.json({error: "invalid answer length"});
            return;
        }
        if (answer.findIndex((item, index) => {
            return item !== (challenge.correct[index] === challenge.expected);
        }) >= 0) {
            res.status(400);
            res.json({error: "Incorrect"});
            return;
        }
        
        stage = challenge.stage + 1;
    }

    if (stage >= stages) {
        res.json({done: true, flag: process.env.CAPTCHA_FLAG});
        return;
    }

    // Generate a new challenge
    let correct = [];
    for (let i = 0; i < 9; ++i) {
        correct.push(randomBool());
    }
    const time = timeLimit(stage);
    const challenge = {stage, expected: randomBool(), correct, expires: Date.now() / 1000 + time};
    const jwe = await new CompactEncrypt(encoder.encode(JSON.stringify(challenge))).setProtectedHeader({ alg: "A128KW", enc: "A256GCM"}).encrypt(challengeKey);
    res.json({challenge: jwe, stage, stages, expected: await generateImage(challenge.expected), images: await Promise.all(challenge.correct.map(input => generateImage(input))), time});
};