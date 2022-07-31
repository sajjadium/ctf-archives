/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */
'use strict';

const { ComponentUtils } = ChromeUtils.import('resource://gre/modules/ComponentUtils.jsm');

const EnterprisePoliciesManager = function() {};

EnterprisePoliciesManager.prototype = {
  classID: Components.ID('{f96da9ad-830b-48ab-9d6e-ecd3738cb89f}'),
  QueryInterface: ChromeUtils.generateQI([
    Ci.nsIObserver,
    Ci.nsISupportsWeakReference,
    Ci.nsIEnterprisePolicies,
  ]),
  _xpcom_factory: ComponentUtils.generateSingletonFactory(EnterprisePoliciesManager),

  // nsIObserver implementation
  observe(/* subject, topic, data */) {},

  // ------------------------------
  // public nsIEnterprisePolicies members
  // ------------------------------

  get status() {
    return Ci.nsIEnterprisePolicies.INACTIVE;
  },

  isAllowed(/* feature */) {
    return true;
  },

  getActivePolicies() {
    return {};
  },

  setSupportMenu(/* supportMenu */) {},

  getSupportMenu() {
    return null;
  },

  setExtensionPolicies(/* extensionPolicies */) {},

  getExtensionPolicy(/* extensionID */) {
    return null;
  },

  setExtensionSettings(/* extensionSettings */) {},

  getExtensionSettings(/* extensionID */) {
    return null;
  },

  mayInstallAddon(/* addon */) {
    return true;
  },

  allowedInstallSource(/* uri */) {
    return true;
  },
};

this.NSGetFactory = ComponentUtils.generateNSGetFactory([EnterprisePoliciesManager]);
