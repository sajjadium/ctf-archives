/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */
'use strict';

const { ComponentUtils } = ChromeUtils.import('resource://gre/modules/ComponentUtils.jsm');

const DisableTelemetryStartup = function() {};

DisableTelemetryStartup.prototype = {
  classID: Components.ID('{b0836913-f33f-4935-96af-235891cd5815}'),
  QueryInterface: ChromeUtils.generateQI([Ci.nsIObserver, Ci.nsITimerCallback]),
  _xpcom_factory: ComponentUtils.generateSingletonFactory(DisableTelemetryStartup),

  observe(/* subject, topic, data */) {},
};

this.NSGetFactory = ComponentUtils.generateNSGetFactory([DisableTelemetryStartup]);
