import { userSchema } from './schema.js'
import { createUser, getUser } from './db.js'
import argon2 from 'argon2'

const DOMAIN = `${process.env.FLY_APP_NAME}.fly.dev`;

export default fastify => {
    fastify.get('/', async (req, res) => {
        return res.view('login.ejs', {
            csrf: await res.generateCsrf()
        });
    });

    fastify.post('/login', {
        schema: userSchema,
        preHandler: fastify.csrfProtection
    }, async (req, res) => {
        let { username, password } = req.body;
        username = `${username}@${DOMAIN}`.toLowerCase();

        const user = getUser(username);
        if (!user) {
            return res.view('error.ejs', { error: 'User not found!' });
        }

        if (!await argon2.verify(user.get('password'), password)) {
            return res.view('error.ejs', { error: 'Wrong password' });
        }

        req.session.user = username;
        return res.redirect('/mail');
    })

    fastify.get('/register', async (req, res) => {
        return res.view('register.ejs', {
            csrf: await res.generateCsrf()
        })
    });

    fastify.post('/register', {
        schema: userSchema,
        preHandler: fastify.csrfProtection
    }, async (req, res) => {
        let { username, password } = req.body;
        username = `${username}@${DOMAIN}`.toLowerCase();

        if (getUser(username)) {
            return res.view('error.ejs', {
                error: 'User already exists!'
            });
        }

        createUser(username, await argon2.hash(password));
        req.session.user = username;

        return res.redirect('/mail');
    });

    fastify.get('/mail', async (req, res) => {
        if (!req.session.user) {
            return res.redirect('/');
        }

        return res.view('mail.ejs', {
            username: req.session.user,
            mail: getUser(req.session.user).get('mail')
        })
    })

}