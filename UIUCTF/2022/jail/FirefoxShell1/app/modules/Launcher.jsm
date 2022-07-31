/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */
'use strict';

const EXPORTED_SYMBOLS = ['Launcher'];

const { Loader } = ChromeUtils.import('resource:///modules/Loader.jsm');

const nativeMapping = {
  '@sdk/': 'resource:///sdk/',
  chrome: 'resource://gre/@chrome',
  loader: 'resource:///@loader',
};

const Launcher = {
  launchMainScript(contentWindow) {
    const require = Loader({
      paths: nativeMapping,
      sandboxPrototype: contentWindow,
    });

    require('@sdk/main.js');
  },
};
