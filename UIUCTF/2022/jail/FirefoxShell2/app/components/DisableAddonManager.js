/* Copyright 2017 Mozilla
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
'use strict';

const { ComponentUtils } = ChromeUtils.import('resource://gre/modules/ComponentUtils.jsm');

const DisabledAddonManager = function() {};

DisabledAddonManager.prototype = {
  classID: Components.ID('{ed6e7c79-fcd3-4285-881e-f0cbb0d8ada0}'),
  QueryInterface: ChromeUtils.generateQI([Ci.nsIObserver, Ci.nsITimerCallback]),
  _xpcom_factory: ComponentUtils.generateSingletonFactory(DisabledAddonManager),

  observe(/* subject, topic, data */) {},
  notify(/* timer */) {},
};

this.NSGetFactory = ComponentUtils.generateNSGetFactory([DisabledAddonManager]);
