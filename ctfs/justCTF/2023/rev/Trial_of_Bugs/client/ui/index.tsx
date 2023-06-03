import * as React from 'react';
import {StrictMode} from 'react';
import {createRoot} from 'react-dom/client';

import App from './App';
import {Client} from "../client";

const rootElement = document.getElementById('app');
const root = createRoot(rootElement!);
const client = new Client();

client.start();

root.render(
    <StrictMode>
        <App client={client} />
    </StrictMode>,
);
