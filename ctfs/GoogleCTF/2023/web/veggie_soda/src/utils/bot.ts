const bot_addr = Deno.env.get("BOT_ADDR") || "localhost"; 
const bot_port = Deno.env.get("BOT_PORT") || 1337; 

export async function visit(url){
    console.log(bot_addr);
    const connection = await Deno.connect({
        port: bot_port,
        hostname: bot_addr,
    });

    const buf = new Uint8Array(100);
    await connection.read(buf);
    await connection.read(buf);
    var res = new TextDecoder().decode(buf);
    console.log(res)
    if (res.includes("Please send me a URL to open.")) {
        const request = new TextEncoder().encode(url+"\n");
        await connection.write(request);
        
    }
    connection.close();
}
