/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */
'use strict';

const { CC } = require('chrome');

const { Configuration } = require('resource:///modules/Configuration.jsm');
const { Exit } = require('resource:///modules/Exit.jsm');

const { AsyncStdin } = require('resource:///modules/AsyncStdin.jsm');
const { Stdout } = require('resource:///modules/Stdout.jsm');

const { REPL } = require('./repl.js');

const browser = document.getElementById('browser');

Stdout.write(`Welcome to ${Configuration.introname}!\n`);

// browser.contentWindow.wrappedJSObject.test = Cu.exportFunction((...args) => Cu.cloneInto(fetch(...args), browser.contentWindow, {cloneFunctions: true}), browser.contentWindow);
// browser.contentWindow.wrappedJSObject.test = fetch;

(async function() {
  const repl = new REPL(
    () => (Configuration.privileged ? Object.getPrototypeOf(window) : browser.contentWindow),
    AsyncStdin,
    Stdout
  );

  await repl.run();
  Exit.exit();
})();
