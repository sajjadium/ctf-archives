import { Hono } from "hono";
import { html } from "hono/html";
import { type PropsWithChildren } from "hono/jsx";
import { MongoClient, ObjectId } from "mongodb";
import { randomUUID, timingSafeEqual } from "node:crypto";

let app = new Hono();
let client = new MongoClient(Bun.env.MONGO_URL!);
async function getDb() {
    await client.connect();
    return client.db("thedatabase");
}

let db = await getDb();
await db.collection("users").deleteMany({});
await db.collection("users").insertMany([
    { name: "Adam", password: randomUUID(), faction: "red" },
    { name: "Bertil", password: randomUUID(), faction: "blue" },
    { name: "Cesar", password: randomUUID(), faction: "blue" },
    { name: "David", password: randomUUID(), faction: "red" },
    { name: "Erik", password: randomUUID(), faction: "red" },
    { name: "Filip", password: randomUUID(), faction: "red" },
    { name: "Gustav", password: randomUUID(), faction: "blue" },
    { name: "Helge", password: randomUUID(), faction: "green" },
    { name: "Ivar", password: randomUUID(), faction: "green" },
    { name: "Johan", password: randomUUID(), faction: "red" },
    { name: "Kalle", password: randomUUID(), faction: "green" },
    { name: "Ludvig", password: randomUUID(), faction: "red" },
    { name: "Martin", password: randomUUID(), faction: "blue" },
    { name: "Niklas", password: randomUUID(), faction: "blue" },
    { name: "Olof", password: randomUUID(), faction: "red" },
    { name: "Petter", password: randomUUID(), faction: "blue" },
    { name: "Qvintus", password: randomUUID(), faction: "blue" },
    { name: "Rudolf", password: randomUUID(), faction: "red" },
    { name: "Sigurd", password: randomUUID(), faction: "red" },
    { name: "Tore", password: randomUUID(), faction: "green" },
    { name: "Urban", password: randomUUID(), faction: "blue" },
    { name: "Viktor", password: randomUUID(), faction: "red" },
    { name: "Wilhelm", password: randomUUID(), faction: "blue" },
    { name: "Xerxes", password: randomUUID(), faction: "red" },
    { name: "Yngve", password: randomUUID(), faction: "blue" },
    { name: "Zäta", password: randomUUID(), faction: "blue" },
    { name: "Åke", password: randomUUID(), faction: "blue" },
    { name: "Ärlig", password: randomUUID(), faction: "red" },
    { name: "Östen", password: randomUUID(), faction: "blue" },
]);

function Page({ children }: PropsWithChildren) {
    let htmlElement = <html>
        <head lang="sv">
            <meta charset="utf-8" />
            <script src="https://unpkg.com/htmx.org@2.0.1" integrity="sha384-QWGpdj554B4ETpJJC9z+ZHJcA/i59TyjxEPXiiUgN2WmTyV5OEZWCD6gQhgkdpB/" crossorigin="anonymous" />
            <script src="https://unpkg.com/htmx-ext-json-enc@2.0.0/json-enc.js" integrity="sha384-jlXY8aqYpGrH/VeBQeCRxt0HdGshtETnnNE2JdPjBsGpZATDeNhwdfPE53pBmVhD" crossorigin="anonymous" />
        </head>
        <body hx-ext="json-enc">
            {children}
        </body>
    </html>;
    return html`<!doctype html>${htmlElement}`;
}

app.get("/", async c => {
    return c.html(<Page>
        <nav>
            <a href="/login">Logga in</a>
        </nav>
        <p>Sök efter personer:</p>
        <form hx-post="/users" hx-target="#result" hx-swap="innerHTML">
            <input placeholder="Name" type="text" name="name" />
            <select
                name="faction"
                hx-on:change="htmx.find('option').disabled = !this.value"
                hx-on:load="htmx.find('option').disabled = !this.value"
            >
                <option disabled selected value="">Filtrera efter lag</option>
                <option value="red">Röd</option>
                <option value="green">Grön</option>
                <option value="blue">Blå</option>
            </select>
            <button>Sök</button>
        </form>
        <div id="result" />
    </Page>);
})

app.post("/users", async c => {
    let db = await getDb();
    let query = await c.req.json();
    query.name = { $regex: query.name, $options: "i" };
    if ("password" in query) return new Response("Bad Request", { status: 400 });
    let users = await db.collection("users").find(query).toArray();
    if (users.length === 0) return c.html(<p>no matches</p>);
    return c.html(<>
        <p>Results:</p>
        <ul>{users.map(user => <li>
            <a href={`/user/${user._id.toString()}`}>{user.name}</a>
        </li>)}</ul>
    </>);
});

app.get("/user/:id", async c => {
    let id: ObjectId;
    try {
        id = new ObjectId(c.req.param("id"));
    } catch (e) {
        return;
    }
    let db = await getDb();
    let user = await db.collection("users").findOne({ _id: id });
    if (!user) return;
    return c.html(<Page>
        <h1>{user.name}</h1>
        <p>Lag: {user.faction}</p>
    </Page>);
});

app.get("/login", async c => {
    return c.html(<Page>
        <form hx-post="/login" hx-swap="textContent">
            <input type="text" name="name" placeholder="username" />
            <input type="password" name="password" placeholder="password" />
            <button>Logga in</button>
        </form>
    </Page>);
});

app.post("/login", async c => {
    let { name, password } = await c.req.json();
    let db = await getDb();
    let user = await db.collection("users").findOne({ name });
    if (!user) return;
    if (password.length !== user.password.length
    || !timingSafeEqual(Buffer.from(password), Buffer.from(user.password))) {
        return new Response("Wrong password", { status: 400 });
    }

    return new Response(Bun.env.FLAG);
});

export default app;
