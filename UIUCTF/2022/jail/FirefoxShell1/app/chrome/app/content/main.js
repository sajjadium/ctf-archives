/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */
'use strict';

window.addEventListener('load', function() {
  const { fallbackLogExc } = ChromeUtils.import('resource:///modules/Utils.jsm');
  const { Exit } = ChromeUtils.import('resource:///modules/Exit.jsm');

  try {
    const { init: consoleInit } = ChromeUtils.import('resource:///modules/ConsoleObserver.jsm');
    consoleInit();

    // We use our own console hooks
    const { Services } = ChromeUtils.import('resource://gre/modules/Services.jsm');
    Services.prefs.setBoolPref('devtools.console.stdout.chrome', false);
    Services.prefs.setBoolPref('browser.dom.window.dump.enabled', false);

    setTimeout(window.minimize, 0);

    const { Launcher } = ChromeUtils.import('resource:///modules/Launcher.jsm');
    Launcher.launchMainScript(window);
  } catch (e) {
    fallbackLogExc(e);
    Exit.exit();
  }
});
