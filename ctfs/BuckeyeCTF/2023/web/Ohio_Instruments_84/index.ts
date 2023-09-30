import { unlink } from "fs/promises";

async function plot(expr: string) {
    if (!/^([x()+*\-\.\^/\d\s]|(\w+\())+$/.test(expr)) {
        throw new Error("Invalid expression");
    }
    const filename = `${crypto.randomUUID()}.jpg`;
    const cmd = `x = -10:.2:10; h = figure('visible', 'off'); plot(x, ${expr}); saveas(h, '${filename}')`;
    const proc = Bun.spawn(["octave", "--eval", cmd])
    let timeout = false;
    setTimeout(() => {
        timeout = true;
        proc.kill();
    }, 10000);
    await proc.exited;
    if (timeout) {
        throw new Error("Timeout");
    }
    if (proc.exitCode !== 0) {
        throw new Error("Octave error");
    }
    setTimeout(async () => {
        await unlink(filename);
    });
    return new Response(Bun.file(filename));
}

const server = Bun.serve({
    port: 1024,
    async fetch(request) {
        const url = new URL(request.url);
        if (url.pathname === "/") {
            return new Response(Bun.file(import.meta.dir + "/index.html"));
        }
        const expr = decodeURI(url.pathname.substring(1));
        return await plot(expr);
    },
    error(error) {
        return new Response(error.message, {
            status: 418
        });
    }
})

console.log(`Listening on port ${server.port}`);