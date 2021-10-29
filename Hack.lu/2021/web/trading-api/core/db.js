const { Pool } = require('pg');
const { getOrDefault } = require('./config');

const DB_URL = getOrDefault('DB_URL', 'postgres://postgres:postgres@localhost:5432/postgres');

async function connect() {
    const client = new Pool({
        connectionString: DB_URL,
    });
    await client.connect();

    return client;
}

function sqlEscape(value) {
    switch (typeof value) {
        case 'string':
            return `'${value.replace(/[^\x20-\x7e]|[']/g, '')}'`;
        case 'number':
            return isFinite(value) ? String(value) : sqlEscape(String(value));
        case 'boolean':
            return String(value);
        default:
            return value == null ? 'NULL' : sqlEscape(JSON.stringify(value));
    }
}

function prepare(query, namedParams) {
    let filledQuery = query;

    const escapedParams = Object.fromEntries(
        Object.entries(namedParams)
              .map(([key, value]) => ([key, sqlEscape(value)]))
    );

    for (const key in escapedParams) {
        filledQuery = filledQuery.replaceAll(`:${key}`, escapedParams[key]);
    }

    return filledQuery;
}

module.exports = {
    connect,
    sqlEscape,
    prepare,
};
