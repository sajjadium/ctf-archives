import Hapi, {Server} from "@hapi/hapi";
import inert from "@hapi/inert"
import {fileURLToPath} from 'url';
import * as Path from "path";
import {index, proxyRequest} from "./handler";
import {checkIpHeader} from "./middleware";

export let server: Server;

export const init = async function (): Promise<Server> {
    server = Hapi.server({
        port: process.env.PORT || 4001,
        host: '0.0.0.0',
        routes: {
            files: {
                relativeTo: Path.join(Path.dirname(fileURLToPath(import.meta.url)), '../static')
            }
        }
    });

    await server.register(inert);

    server.ext('onRequest', checkIpHeader)

    // Static files
    server.route({
        method: 'GET', path: '/',
        handler: index
    })

    server.route({
        method: 'GET', path: '/public/{param*}',
        handler: {
            directory: {path: 'public'}
        }
    })

    server.route({
        method: 'GET', path: '/proxy/{endpoint}',
        handler: proxyRequest
    })

    return server;
};

export const start = async function (): Promise<void> {
    console.log(`Listening on ${server.settings.host}:${server.settings.port}`);
    return server.start();
};
