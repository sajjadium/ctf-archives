/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */
'use strict';

const { ComponentUtils } = ChromeUtils.import('resource://gre/modules/ComponentUtils.jsm');
const { Services } = ChromeUtils.import('resource://gre/modules/Services.jsm');
const { Configuration } = ChromeUtils.import('resource:///modules/Configuration.jsm');

/**
 * The main command line handler
 */
const CommandLine = function() {};

CommandLine.prototype = {
  classID: Components.ID('{00995ba2-223f-4efb-b656-ce98aff7019b}'),
  classDescription: 'Command line handler',
  QueryInterface: ChromeUtils.generateQI([Ci.nsICommandLineHandler]),

  // ------- nsICommandLineHandler interface

  handle(cmdLine) {
    Services.cache2.clear();

    Configuration.privileged = cmdLine.handleFlag('privileged', true);
    Configuration.hardened = cmdLine.handleFlag('hardened', true);
    Configuration.introname = cmdLine.handleFlagWithParam('introname', true);

    if (!Configuration.introname || !Configuration.introname.length) {
      Configuration.introname = 'Gecko CLI';
    }
  },
};

this.NSGetFactory = ComponentUtils.generateNSGetFactory([CommandLine]);
