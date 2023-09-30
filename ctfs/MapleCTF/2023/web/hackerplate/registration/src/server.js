import express from 'express'
import bodyParser from 'body-parser'
import { renderFile } from 'ejs';
import VehicleRegistration from './vehicle-registration.js';
import DBFactory from './db.js';
import { findPlateIndices, parseStringAsValue, toPDF, validVIN } from './util.js';
import { v4 as uuidv4} from 'uuid';

const SECRET = process.env.SECRET || "deadbeef"
const INTERNAL_PORT = process.env.INTERNAL_PORT || 4401;
const BASE = process.env.BASE || `http://localhost:${INTERNAL_PORT}`

const server = express();

server.use(bodyParser.urlencoded({ extended: true }));
server.set('view engine', 'ejs');
server.engine('html', renderFile);

server.use(express.static('public'));

let inFlightRequests = {}

server.get("/", (req, res) => {
    res.render('index.ejs');
});

server.post('/register-vehicle', async (req, res) => {
    try {
        const { name, pid, birthdate, vin, ...rest } = req.body;
        if (!name || !pid || !birthdate || !vin) {
            res.status(400).send("missing required fields");
            return;
        }
        if (!validVIN(vin)) {
            console.log("invalid vin")
            res.status(400).send("invalid vin")
            return
        }
        if (vin in inFlightRequests) {
            res.status(400).send("process already underway")
            return
        }
        const db = await DBFactory.getDB();
        if (!await db.canRegisterVehicle(vin)) {
            res.status(400).send("vehicle already registered")
            return
        }
        inFlightRequests[vin] = new VehicleRegistration(name, pid, birthdate, vin);
        await inFlightRequests[vin].addUser()
        console.log("registered user")
        res.send("ok, send user to plate selection station")
        return;
    } catch (e) {
        console.log(e);
        res.send("err")
        return;
    }
});

server.get('/download-report', async (req, res) => {
    const vin = req.query.vin;
    const style = req.query.style ?? "formal";
    const opts = {}
    if (!vin) {
        res.status(400).send("no vin provided");
        return;
    }
    for (const [key, value] of Object.entries(req.query)) {
        if (key !== "vin" && key !== "style") {
            opts[key] = parseStringAsValue(value);
        }
    }
    const db = await DBFactory.getDB();
    const user = await db.getUserByVIN(vin) ?? {};
    const vehicle = await db.getVehicleByVIN(vin) ?? {};

    const userData = [
        ["Vehicle IN", vin],
        ["Owner", user.name ?? "Not Found"],
        ["Plate", vehicle.plate ?? "Not Found"]
    ]

    const vehicleParams = [
        ["Make", vehicle.make ?? "Not Found"],
        ["Model", vehicle.model ?? "Not Found"],
        ["Year", vehicle.year ?? "Not Found"],
    ]

    const formattedDate = new Date().toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric"
    });

    res.render('pdf.ejs', { style: style, base: BASE, date: formattedDate, userData: userData, vehicleParams: vehicleParams }, async (err, html) => {
        if (err) {
            console.log(err);
            res.status(500).send("error rendering pdf");
        } else {
            const pdf = await toPDF(html, style, opts);
            if (pdf) {
                res.setHeader('Content-Type', 'application/pdf');
                res.send(pdf);
            } else {
                res.status(500).send("error rendering pdf");
            }
        }
    return;
    });
});

server.get('/healthz', (req, res) => {
    res.send("ok");
});

// lottery server endpoints

server.get('/lottery/attempt', async (req, res) => {
    if (req.query.secret !== SECRET) {
        res.status(403).send("invalid secret");
        return;
    }
    if (!req.query.vin) {
        res.status(400).send("no vin provided");
        return;
    }
    if (!(req.query.vin in inFlightRequests)) {
        res.status(404).send("no registration found for this vehicle");
        return;
    }
    if (inFlightRequests[req.query.vin].isAttempting()) {
        res.status(403).send("already attempting");
    }
    const db = await DBFactory.getDB();
    const platesRegistered = await db.getLicensePlates();
    // sends a list of indices of plates that have been taken
    res.send({
        plates: findPlateIndices(platesRegistered)
    });
});

server.post('/lottery/cancel', (req, res) => {
    if (req.body.secret !== SECRET) {
        res.status(403).send("invalid secret");
        return;
    }
    if (!req.body.vin) {
        res.status(400).send("no vin provided");
        return;
    }
    if (!(req.body.vin in inFlightRequests)) {
        res.status(404).send("no registration found for this vehicle");
        return;
    }
    if (inFlightRequests[req.body.vin].isAttempting()) {
        inFlightRequests[req.body.vin].cancelAttempt();
    }
    res.send("ok");
});

server.post('/lottery/complete', async (req, res) => {
    if (req.body.secret !== SECRET) {
        res.status(403).send("invalid secret");
        return;
    }
    const registration = inFlightRequests[req.body.vin ?? ""] ?? null;
    if (!registration) {
        res.status(404).send("no registration found for this vehicle");
        return;
    }
    await inFlightRequests[req.body.vin].finalize(req.body.plate);
    delete inFlightRequests[req.body.vin];
    res.send("ok");
});

setInterval(() => {
    for (const vin in inFlightRequests) {
        if (inFlightRequests[vin].expired()) {
            inFlightRequests[vin].rollback();
            delete inFlightRequests[vin];
        }
    }
}, 1000 * 10) // check every 10 seconds

DBFactory.getDB(); // initialize db

export default server;