const assetsManifest = require('../build/asset-manifest.json');
const normalizePath = path => path.replace(/(?<!:)\/\//g, '/');
const joinPath = (...paths) => normalizePath(paths.join('/'));
const rootPath = '';

const manifest = `<link rel="manifest" href="${joinPath(
    rootPath,
    'manifest.json'
)}">`;
const favicon = `<link rel="shortcut icon" href="${joinPath(
    rootPath,
    'favicon.ico'
)}">`;

const scripts = Object.keys(assetsManifest.files).reduce((accumulated, key) => {
    const jsFile = assetsManifest.files[key];
    return (
        accumulated +
        (jsFile.endsWith('.js')
            ? `<script src="${joinPath(rootPath, jsFile)}"></script>`
            : '')
    );
}, '');

const css = Object.keys(assetsManifest.files).reduce((accumulated, key) => {
    const cssFile = assetsManifest.files[key];
    return (
        accumulated +
        (cssFile.endsWith('.css')
            ? `<link href="${joinPath(rootPath, cssFile)}" rel="stylesheet" />`
            : '')
    );
}, '');

module.exports = { css, scripts, favicon, manifest };
