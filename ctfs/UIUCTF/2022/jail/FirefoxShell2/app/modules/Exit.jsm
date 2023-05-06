/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */
'use strict';

const EXPORTED_SYMBOLS = ['Exit'];

const { Services } = ChromeUtils.import('resource://gre/modules/Services.jsm');
const { AsyncStdin } = ChromeUtils.import('resource:///modules/AsyncStdin.jsm');

const Exit = {
  exit() {
    if (this.exiting) {
      return;
    }

    this.exiting = true;
    AsyncStdin.terminate();
    Services.startup.quit(Ci.nsIAppStartup.eForceQuit);
  },

  exiting: false,
};
