import express, { text } from "express";
import { readFileSync } from "fs";
import { spawn } from "child_process";

import { bufToBlock } from "../base/block";
import { build, fromBlocks } from "../base/repository";

const recievedBlocks: [bigint, string][] =  [
	[
		0x3a05bn,
		"00000000000000000000000000000000|1:[@0-0+ca(0a636f6e73742066696c6550617468203d20222e2f666c61672e747874223b0a636f6e73742066696c6544617461203d20226263616374667b74656d705f666c61677d223b0a0a636f6e737420666c616756616c696461746f725265676578203d202f6263616374665c7b5b612d7a412d5a302d395f5c2d5d2b2f3b0a0a696620282166696c65446174612e7472696d28292e6d6174636828666c616756616c696461746f725265676578292920636f6e736f6c652e6c6f67282262616420666c6167203a2822293b0a)]"
	],
	[
		0x3a5f5n,
		"00000000000000000000000000017405|3:[@1-0+33(696d706f7274207b7265616446696c6553796e63206173207265616446696c657d2066726f6d20276e6f64653a6673273b0a0a)][@53-0+20(2f2f2041637475616c6c7920726561642074686520666c61672066696c652e0a)][@84-13+1a(7265616446696c652866696c65506174682c2022757466382229)]"
	],
	[
		0x3587an,
		"0000000000000000000000000003a5f5|2:[@105-1+0()][@130-1c+7c(7b0a20202020636f6e736f6c652e6c6f672822466c6167204d61746368657322293b0a7d20656c7365207b0a20202020636f6e736f6c652e6c6f672822466c616720646f6573204e4f54206d61746368203a2822293b0a20202020636f6e736f6c652e6c6f672822466c61673a222c2066696c6544617461293b0a7d)]"
	],
] ;

const server = express();

const index = readFileSync("server/index.html", "utf-8");


server.use(text());

server.get(
    "/",
    async (_, res) => {
        res.send(index);
    }
);
server.post(
    "/submit",
    async (req, res) => {
        const body = req.body;
        if (typeof body !== "string") {
            res.status(400).send("Bad Body");
            return;
        }
        console.log("Submit req recieved with body:", body.slice(0, 1024));

        const buffer = Buffer.from(body);
        const block = bufToBlock(buffer);

        if (!block) {
            res.status(400).send("Malformed Block");
            return;
        }

        const repo = fromBlocks([
            bufToBlock(Buffer.from(recievedBlocks[0][1]))!,
            block,
            bufToBlock(Buffer.from(recievedBlocks[1][1]))!,
            bufToBlock(Buffer.from(recievedBlocks[2][1]))!,
        ]);

        const output = build(repo);
        if (!output) {
            res.status(400).send("Corruption or tampering detected...\n\nHOW DARE YOUUUUU..........");
            return;
        }

        const controller = spawn("deno", ["run", "--allow-read=./flag.txt", "-"]);
        
        controller.stdin.write(output.toString("ascii") + "\n");
        controller.stdin.end();
        
        controller.stderr.pipe(process.stderr, { end: false });

        res.write("Output:\n");
        controller.stdout.pipe(res);
    }
);


server.listen(8080, () => console.log("Listening on 8080"));
