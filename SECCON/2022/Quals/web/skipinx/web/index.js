const app = require("express")();

const FLAG = process.env.FLAG ?? "SECCON{dummy}";
const PORT = 3000;

app.get("/", (req, res) => {
  req.query.proxy.includes("nginx")
    ? res.status(400).send("Access here directly, not via nginx :(")
    : res.send(`Congratz! You got a flag: ${FLAG}`);
});

app.listen({ port: PORT, host: "0.0.0.0" }, () => {
  console.log(`Server listening at ${PORT}`);
});
