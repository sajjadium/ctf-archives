const express = require('express');
require('express-async-errors');
config = require('config');

if (process.env.DATABASE_HOST !== null) {
    console.log(`Found custom database host: ${process.env.DATABASE_HOST}`);
    config.knex.connection.host = process.env.DATABASE_HOST;
}

const app = express();
const port = 3001;
const knex = require('knex')(config.get('knex'));

knex.schema.hasTable('crushes').then(function(exists) {
    if (!exists) {
        console.log("crushes table doesn't exist, initializing...");
        knex.schema.createTable('crushes', function(table) {
            table.increments('id').primary();
            table.string('from').notNullable();
            table.string('to').notNullable();
            table.string('message').notNullable();
            table.index(['to']);
        }).then();
        knex('crushes').insert({
            from: config.init.flag,
            to: config.init.flag,
            message: 'This is the flag!',
        }).then();
    }
});

app.use(express.static('html'));
app.use(express.json());
app.use(express.urlencoded({
    extended: false
}));

app.get('/debug', async (req, res) => {
    // poor man's clone
    const c = JSON.parse(JSON.stringify(config.get('knex')));
    if (c.connection.password) {
        c.connection.password = "*******";
    }
    res.status(200).send(c);
})


app.post('/record', async (req, res) => {
    if (req.body.from && req.body.to && req.body.message) {
        await knex('crushes').insert({
            from: req.body.from,
            to: req.body.to,
            message: req.body.message,
        });
        res.status(200).send({});
    } else {
        res.status(400).send({});
    }
});

app.post('/data', async (req, res) => {
    if (req.body.to) {
        const crushes = await knex('crushes')
            .select()
            .where({
                to: req.body.to
            })
            .limit(50);
        res.send(crushes);
    } else {
        res.status(400).send({});
    }
});

app.use((err, req, res, next) => {
    console.error(err);
    res.status(400).send({
        error: err.message
    });
});

app.listen(port, () => {
    console.log(`Listening on port ${port} in ${process.env.NODE_ENV}`);
});
