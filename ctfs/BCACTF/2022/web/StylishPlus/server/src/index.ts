import fastify from 'fastify';
import { Static, Type } from '@sinclair/typebox';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import fastifyStatic from '@fastify/static';
import cuid from 'cuid';
import puppeteer, { BrowserContext, Page } from 'puppeteer';
import { readFileSync } from 'fs';

const flag = readFileSync(join(dirname(fileURLToPath(import.meta.url)), "../../flag.txt"), "utf8");

const app = fastify({ logger: true });
const browser = puppeteer.launch({ args: ["--no-sandbox"] });

const chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"];
for (let i = 0; i < chars.length - 1; i++) {
    let temp = chars[i];
    let j = Math.floor(Math.random() * (chars.length - i)) + i;
    chars[i] = chars[j];
    chars[j] = temp;
}
const thePasscode = chars.join("");
console.log(thePasscode);

app.register(fastifyStatic, {
    root: join(dirname(fileURLToPath(import.meta.url)), "../../public"),
});

const Theme = Type.Object({
    bodyBG: Type.String({
        maxLength: 5000,
    }),
    bodyFG: Type.String({
        maxLength: 5000,
    }),
    accentBG: Type.String({
        maxLength: 5000,
    }),
    accentFG: Type.String({
        maxLength: 5000,
    }),
});

const FlagRequest = Type.Object({
    passcode: Type.String(),
});

const themes = new Map();

app.get<{ Params: { id: string }, Reply: Static<typeof Theme> | { error: string } }>("/api/theme/:id", (request, reply) => {
    const theme = themes.get(request.params.id);
    if (theme) {
        reply.send(theme);
    } else {
        reply.code(404).send({
            error: "Theme not found",
        });
    }
});

app.post<{ Body: Static<typeof Theme> }>("/api/report", async (request, reply) => {
    // Generate an ID
    const id = cuid();

    // Store the theme
    themes.set(id, request.body);

    let context: BrowserContext | undefined;
    let page: Page | undefined;

    try {
        context = await (await browser).createIncognitoBrowserContext();
        page = await context.newPage();
        await page.setCacheEnabled(false);
        await page.goto(`http://localhost:3000/?theme=${id}`, { waitUntil: "load", timeout: 3000 });
        await page.click("#open-admin-panel");

        // Wait a bit to give everything some time to load
        await new Promise(resolve => setTimeout(resolve, 1000));

        const passcode = thePasscode;
        for (let i = 0; i < passcode.length; i++) {
            const char = passcode.charAt(i);
            const id = cuid();
            await page.evaluate(`
            document.querySelectorAll("#keypad > button").forEach(button => {
                if (button.innerText === "${char}") {
                    button.id = "${id}";
                }
            })
            `);
            await page.click(`#${id}`);
            await new Promise(resolve => setTimeout(resolve, 300));
        }

        const submitID = cuid();
        await page.evaluate(`
        document.querySelectorAll("#keypad > button").forEach(button => {
            if (button.innerText === "Submit") {
                button.id = "${submitID}";
            }
        })
        `);
        await page.click(`#${submitID}`);
        await new Promise(resolve => setTimeout(resolve, 3000));

        reply.send("sure");
    } catch (e) {
        console.error(e);
        throw e;
    } finally {
        // Clean up
        themes.delete(id);
        await page?.close();
        await context?.close();
    }
});

app.post<{ Body: Static<typeof FlagRequest> }>("/api/flag", {
    schema: {
        body: FlagRequest,
    },
}, (request, reply) => {
    const { passcode } = request.body;
    if (passcode === (thePasscode ?? "")) {
        console.log("Flag get!");
        reply.send(flag ?? "yell at the problem author to fix this");
    } else {
        reply.status(403).send("no");
    }
});

try {
    await app.listen(3000, "0.0.0.0");
} catch (err) {
    app.log.error(err);
    process.exit(1);
}