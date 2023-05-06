
// Wrap everything in a function to force database initialization first

async function main() {

    const express = require("express");
    const cookieParser = require("cookie-parser");
    const csv = require("csvtojson");
    const crypto = require('crypto');
    const {Sequelize, DataTypes, Op} = require("sequelize");
    const sequelize = new Sequelize(`postgres://${process.env.POSTGRES_USER}:${process.env.POSTGRES_PASSWORD}@db`, {logging: true});
    const app = express();
    app.use(cookieParser());
    app.set('views', './views');
    app.set('view engine', 'pug');

    const port = process.env.PORT;

    /**
     * Translates seconds into human readable format of seconds, minutes, hours, days, and years
     *
     * @param  {number} seconds The number of seconds to be processed
     * @return {string}         The phrase describing the amount of time
     * Source: https://stackoverflow.com/a/34270811
     */
    function forHumans(seconds) {
        var levels = [
            [Math.floor(seconds / 31536000), 'years'],
            [Math.floor((seconds % 31536000) / 86400), 'days'],
            [Math.floor(((seconds % 31536000) % 86400) / 3600), 'hours'],
            [Math.floor((((seconds % 31536000) % 86400) % 3600) / 60), 'minutes'],
            [(((seconds % 31536000) % 86400) % 3600) % 60, 'seconds'],
        ];
        var returntext = '';

        for (var i = 0, max = levels.length; i < max; i++) {
            if (levels[i][0] === 0) continue;
            returntext += ' ' + levels[i][0] + ' ' + (levels[i][0] === 1 ? levels[i][1].substr(0, levels[i][1].length - 1) : levels[i][1]);
        };
        return returntext.trim();
    }

    // position of last served; used for position calculations without bulk updating position numbers in database
    let currentlyServing = 0;

    const Queue = sequelize.define('Queue', {
        uuid: {
            type: DataTypes.UUID,
            primaryKey: true
        },
        position: {
            type: DataTypes.BIGINT,
            allowNull: false,
            unique: true
        },
        served: {
            type: DataTypes.BOOLEAN,
            defaultValue: false,
            allowNull: false
        }
    }, {
        timestamps: false
    });


    // Make sure previous users exist and table is up-to-date with at least 17600 waiting users in the queue already 😈
    // If you are wondering why that number, I originally chose 20000 but that didn't work out for *reasons* so I used a random number generator and got this
    await Queue.sync({alter: true});

    const response = await Queue.count({
        where: {
            position: {
                [Op.lte]: 17676
            },
            served: false
        }
    });
    if (response < 17600) {
        await Queue.drop()
        await Queue.sync({force: true});
        const dummyData = await csv().fromFile("dummy_data.csv");
        await Queue.bulkCreate(dummyData);

    }


    // "serve" one user every 5 minutes starting at the beginning of the ctf
    const interval = 5 * 60 * 1000;
    serveUser();
    setInterval(serveUser, interval);

    async function serveUser() {
        if (Date.now() < process.env.startTime) {
            console.log("CTF has not started yet");
        } else {
            const served = (await sequelize.query("select * from public.\"Queues\" where position = (select min(position) from public.\"Queues\" where served = false);", {
                model: Queue,
                mapToModel: true
            }))[0];
            Queue.update({served: true}, {
                where: {uuid: served.uuid}
            });
            console.log("Served UUID " + served.uuid);
            currentlyServing = served.position;
        }
    }


    // Main page
    // See if UUID exists and is in db, if not, assign a new one
    // Then fetch info on queue status, giving basic info and a button to press when the queue is over
    app.get("/", async function (req, res) {
        let uuid = req.cookies["uuid"];
        let position;
        if (uuid !== undefined) {
            let user;
            // Make sure uuid is actually in the database
            try {
                if (uuid.length != 36) {
                    user = null;
                } else {
                    user = await Queue.findByPk(uuid);
                }
            } catch {
                user = null
            }
            if (user === null) {
                res.clearCookie("uuid");
                uuid = undefined;
            } else if (user.served === true) {
                res.render('flagredirect', {uuid: uuid, flagserverurl: process.env.FLAG_SERVER_URL});
                return;
            } else {
                position = user.position;
            }
        }
        if (uuid === undefined) {

            uuid = crypto.randomUUID();
            res.cookie("uuid", uuid);
            await sequelize.query(`insert into public."Queues" (uuid, position) values ('${uuid}', (select max(position) + 1 from "Queues"));`);
            console.log("Added new uuid of " + uuid);
            position = (await Queue.findByPk(uuid)).position;
            console.log(position);
        }
        const relPos = position - currentlyServing;
        res.render('index', {title: `Queue Pos: ${relPos}`, position: relPos, time: forHumans(relPos * 5 * 60)});
    });

    // Middleware to restrict api by api key
    const adminOnly = function (req, res, next) {
        const authHeader = req.get("Authorization");
        if (authHeader === `Bearer ${process.env.ADMIN_SECRET}`) {
            next();
        } else {
            res.status(403);
            res.send("Either this page doesn't exist or you don't have permission to view this page.");
        }
    }

    app.use(adminOnly);

    app.get("/api/heartbeat", async (req, res) => {
        res.send("online");

    });

    app.get("/api/:uuid/status", async (req, res) => {
        try {
            const user = await Queue.findByPk(req.params.uuid);
            res.send(user.served);

        } catch {
            res.send("false");
        }

    });

    app.get("/api/:uuid/bypass", async (req, res) => {
        try {
            const user = await Queue.findByPk(req.params.uuid);
            if (user === undefined) {
                res.send("uuid not found");
            } else {
                await user.update({served: true});
                res.send("bypassed");
            }
        } catch {
            res.send("invalid uuid");
        }

    });


    app.listen(port, () => {
        console.log(`Listening on port ${port}`);
    });
}
main();