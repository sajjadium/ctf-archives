const express = require('express');
const morgan = require('morgan');

const { getOrDefault } = require('./config');
const { login, authn } = require('./authn');
const { authz, Permissions } = require('./authz');
const registerApi = require('./api');

const HOST = getOrDefault('HOST', '127.0.0.1');
const PORT = getOrDefault('PORT', '3000');

async function main() {
    const app = express();
    
    app.use(morgan('dev'));
    app.use(express.json());

    app.all('/health', (req, res) => res.send('ok'));
    
    // authentication
    app.post('/api/auth/login', login);
    app.use(authn);
    
    // authorization
    app.use(authz({
        userPermissions: new Map(Object.entries({
            warrenbuffett69: [Permissions.VERIFIED],
        })),
        routePermissions: [
            [/^\/+api\/+priv\//i, Permissions.VERIFIED],
        ],
    }));
    
    await registerApi(app);
    
    app.listen(PORT, HOST, () => console.log(`Listening on ${HOST}:${PORT}`));
}

main();
