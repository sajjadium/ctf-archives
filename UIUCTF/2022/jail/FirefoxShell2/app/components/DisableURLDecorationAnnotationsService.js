/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */
'use strict';

const { ComponentUtils } = ChromeUtils.import('resource://gre/modules/ComponentUtils.jsm');

const URLDecorationAnnotationsService = function() {};

URLDecorationAnnotationsService.prototype = {
  classID: Components.ID('{768ae831-5722-4969-b391-b9e8b06d58d2}'),
  QueryInterface: ChromeUtils.generateQI([Ci.nsIObserver, Ci.nsIURLDecorationAnnotationsService]),

  // nsIObserver implementation
  observe(/* subject, topic, data */) {},

  // ------------------------------
  // public nsIURLDecorationAnnotationsService members
  // ------------------------------

  ensureUpdated() {
    return Promise.resolve();
  },
};

this.NSGetFactory = ComponentUtils.generateNSGetFactory([URLDecorationAnnotationsService]);
