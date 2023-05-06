const dotenv = require('dotenv');
dotenv.config();

const getRequired = (key) => {
    if (!process.env.hasOwnProperty(key)) {
        console.error(`Missing config: ${key}`);
        process.exit(1);
    }

    return process.env[key];
};

const getOrDefault = (key, defaultValue) => {
    if (!process.env.hasOwnProperty(key)) {
        return defaultValue;
    }

    return process.env[key];
}

const getOrGenerate = (key, generator) => {
    if (!process.env.hasOwnProperty(key)) {
        const generated = generator();
        console.log(`Using generated value: ${key}=${generated}`);
        process.env[key] = generated;
        return generated;
    }

    return process.env[key];
}

module.exports = {
    getRequired,
    getOrDefault,
    getOrGenerate,
};
