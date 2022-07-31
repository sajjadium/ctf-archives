/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */

// This is to silence the sessionstore errors, see eg:
// https://bugzilla.mozilla.org/show_bug.cgi?id=1578296
// JavaScript error: resource://gre/modules/SessionStoreFunctions.jsm,
// line 120: NS_ERROR_FILE_NOT_FOUND:

'use strict';

const EXPORTED_SYMBOLS = ['SessionStore'];

const SessionStore = {
  maybeExitCrashedState(browser) {},
  updateSessionStoreFromTablistener(aBrowser, aBrowsingContext, aPermanentKey, aData) {},
};
