import * as React from 'react';
import {GameLoaderUi} from "./GameLoaderUi";
import {Game} from "./Game";
import {useObservableField} from "../util/useObservableField";
import {Client} from "../client";
import {Connection} from "../connection";
import {LOGIN_ERROR_TEXT} from "../../share/net/login_errors";
import "./App.css";

export default function App({client}: {client: Client}) {
    let loading = !useObservableField(client.loadComplete);
    let connectError = useObservableField(client.connectError);
    const connection: Connection|null|undefined = useObservableField(client.connection); // TODO: why is this needed?
    const connectState = useObservableField(connection?.connectState);
    const disconnected = useObservableField(connection?.disconnected);

    return (
        <>
            {loading && <GameLoaderUi loader={client.loader} />}
            {!loading && !connection && !connectError && <h1 className="load-status">Connecting…</h1>}
            {connectState === 'connecting' && <h1 className="load-status">Logging in…</h1>}
            {connectState === 'connected' && <Game connection={connection!} />}
            {connectState === 'login_error' && (
                <div className="error-screen">
                    <h1>Login error</h1>
                    <p>{LOGIN_ERROR_TEXT[connection!.loginError!] || 'An unknown error has occurred'}</p>
                    <p className="error-footer">{connection!.net.toString()} - {connection!.loginError!}</p>
                </div>
            )}
            {connectError && (
                <div className="error-screen">
                    <h1>Connection error</h1>
                    <p>Failed to connect to the server.</p>
                </div>
            )}
            {!connectError && connectState !== 'login_error' && disconnected && (
                <div className="disconnect-warning">Disconnected</div>
            )}
        </>
    );
}
