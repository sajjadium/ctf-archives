export default async function handler(req, res) {
    
    res.statusCode = 200;
    res.setHeader(
        "Set-Cookie",
        "session=x; Path=/; HttpOnly; SameSite=Strict; expires=Tue, 09 Jul 1337 15:04:50 GMT"
    );
    res.end();
}
