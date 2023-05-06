'use strict';

const express = require('express')
const app = express()
const Joi = require('joi');

const db = require('./db.js');


process.on('SIGINT', function() {
    console.log( "\nGracefully shutting down from SIGINT (Ctrl-C)" );
    process.exit(1);
});


function createAccountSchema(req, res, next) {
    const schema = Joi.object({
        name: Joi.string().required(),
        password: Joi.string().required(),
        public_key: Joi.string().optional(),
    })
    validateRequest(req, next, schema);
}


function createAccount(req, res) {
    const e2e ='public_key' in req.body;
    try {
        db.add_user(req.body.name, req.body.password, e2e, req.body.public_key);
    } catch (error) {
        return res.status(400).json({error: error.toString()});
    }

    return res.json({message: 'user created'});
}


function userLookup(req, res) {
    var user = db.get_user(req.params.name);
    if (!user) {
        return res.status(400).json({error: "user doesn't exist"});
    }

    return res.json({user: {name: user.name, public_key: user.get_public_key('hex'), e2e: user.e2e, hidden: user.hidden}});
}


function listUsers(req, res) {
    const users = db.list_users();
    return res.json({users: users});
}

function deserializeAuthToken(authToken) {
  const [username, password] = Buffer.from(authToken.split(" ")[1], 'base64').toString().split(":", 2); // XXX: the password can't contain ':'
  return { username, password };
}

function checkAuth(req, res) {
  const credentials = deserializeAuthToken(req.headers.authorization)
  const { username, password } = credentials;
  const user = db.get_user(username);
  const isAuthenticated = !!user && user.password === password;
  return res.status(200).send({ isAuthenticated });
}

function authenticate(req, res, next) {
    if (!req.headers.authorization) {
        return res.status(403).json({error: 'invalid credentials'});
    }
    const credentials = deserializeAuthToken(req.headers.authorization);
    const { username, password } = credentials;

    var user = db.get_user(username);
    if (!user || user.password != password) {
        return res.status(400).json({error: 'invalid credentials'});
    }

    if (username == 'jane' && req.method.toLowerCase() != 'get') {
        return res.status(400).json({error: "jane is a demo account, you can't do that."});
    }

    res.locals.user = user;
    next();
}

function getCurrentUser(req, res) {
  const { user } = res.locals;
  return res.json({user: {name: user.name, public_key: user.get_public_key('hex'), e2e: user.e2e, hidden: user.hidden}});
}

function messageSendSchema(req, res, next) {
    const schema = Joi.object({
        to: Joi.string().required(),
        message: Joi.string().required(),
        iv: Joi.number()
            .min(0)
            .max(0xffffffffffffffffffffffffffffffff)
            .optional(),
    });
    validateRequest(req, next, schema);
}


function messageSend(req, res) {
    try {
        res.locals.user.send_message(req.body.to, req.body.message, req.body.iv)
    } catch (error) {
        return res.status(400).json({error: error.toString()});
    }

    return res.json({message: 'message sent'});
}


function updateSettingsSchema(req, res, next) {
    const schema = Joi.object({
        hidden: Joi.boolean().optional(),
        password: Joi.string().optional(),
    });
    validateRequest(req, next, schema);
}


function updateSettings(req, res) {
    db.update_settings(res.locals.user, req.body);
    res.json({message: 'settings updated'});
}


function deleteUser(req, res) {
    db.delete_user(res.locals.user);
    return res.json({message: 'user deleted'});
}


function listMessages(req, res) {
    const start = (req.params.start !== undefined) ? parseInt(req.params.start) : undefined;
    const end = (req.params.end !== undefined) ? parseInt(req.params.end) : undefined;
    return res.json({messages: res.locals.user.get_message_list(start, end)});
}


function getMessage(req, res) {
    var id = parseInt(req.params.id);
    var message = res.locals.user.get_message(id);
    if (message == null) {
        return res.status(400).json({error: 'invalid message id'});
    }
    return res.json({message: message});
}


function validateRequest(req, next, schema) {
    const options = {
        abortEarly: false, // include all errors
        allowUnknown: true, // ignore unknown props
        stripUnknown: true // remove unknown props
    };
    const { error, value } = schema.validate(req.body, options);
    if (error) {
        next(`Validation error: ${error.details.map(x => x.message).join(', ')}`);
    } else {
        req.body = value;
        next();
    }
}

app.use(express.json());

app.post("/api/message/send", authenticate, messageSendSchema, messageSend);

app.get("/api/user/lookup/:name", userLookup);

app.post("/api/user/settings", authenticate, updateSettingsSchema, updateSettings);

app.get("/api/message/list", authenticate, listMessages);
app.get("/api/message/list/:start(\\d+)", authenticate, listMessages);
app.get("/api/message/list/:start(\\d+)-:end(\\d+)", authenticate, listMessages);
app.get("/api/auth", checkAuth);
app.get("/api/user/me", authenticate, getCurrentUser);

app.get("/api/message/:id", authenticate, getMessage);

app.get("/api/user/list", listUsers);

app.post("/api/user/signup", [createAccountSchema, createAccount]);

app.delete("/api/user/delete", authenticate, deleteUser);

app.use('/assets/', express.static('/front/assets/'));
app.use(express.static('/', {index: ['front/index.html']}));

app.listen(8001, () => { console.log("[*] server started") });
