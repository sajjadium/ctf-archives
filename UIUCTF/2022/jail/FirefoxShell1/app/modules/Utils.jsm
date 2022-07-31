/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */
'use strict';

const EXPORTED_SYMBOLS = [
  'fallbackLogExc',
  'setTimeoutXPCOM',
  'clearTimeoutXPCOM',
  'syncWaitPromise',
  'sleepNonBlocking',
  'sleepBlocking',
];

const { Constructor: CC } = Components;

const { Services } = ChromeUtils.import('resource://gre/modules/Services.jsm');
const { Stdout } = ChromeUtils.import('resource:///modules/Stdout.jsm');

/* global OS */
const { ctypes } = ChromeUtils.import('resource://gre/modules/ctypes.jsm');
Cc['@mozilla.org/net/osfileconstantsservice;1'].getService(Ci.nsIOSFileConstantsService).init();

const libc = ctypes.open('libc.so.6');
const LIBC = OS.Constants.libc;
const timespec = ctypes.StructType('timespec', [{ tv_sec: ctypes.long }, { tv_nsec: ctypes.long }]);
const nanosleep = libc.declare(
  'nanosleep',
  ctypes.default_abi,
  ctypes.int,
  timespec.ptr,
  timespec.ptr
);

const Timer = CC('@mozilla.org/timer;1', 'nsITimer');
const PrefService = Services.prefs;

const fallbackDump = function(str) {
  try {
    Stdout.write(str);
  } catch (e) {
    try {
      PrefService.setBoolPref('browser.dom.window.dump.enabled', true);
    } catch (e) {}

    dump(str);
  }
};

const fallbackLogExc = function(ex) {
  fallbackDump('Error during the script execution\n');

  if (typeof ex === 'object') {
    fallbackDump(`[Exception] ${ex}`);

    if ('fileName' in ex) {
      fallbackDump(`  filename:${ex.fileName}`);
    }
    if ('lineNumber' in ex) {
      fallbackDump(`  line:${ex.lineNumber}`);
    }

    fallbackDump('\n');
  } else {
    fallbackDump(`[Exception] ${ex}\n`);
  }

  let stackText = '\nStack trace:\n';
  let count = 0;
  let stack = ex.stack || Components.stack.caller;
  while (stack) {
    stackText += count++ + ':' + stack + '\n';
    stack = stack.caller;
  }
  fallbackDump(stackText);
};

const setTimeoutXPCOM = function(func, delay, ...args) {
  const timer = new Timer();

  timer.initWithCallback(
    {
      QueryInterface: ChromeUtils.generateQI([Ci.nsITimerCallback]),
      notify() {
        func.apply(undefined, args);
      },
    },
    delay,
    Ci.nsITimer.TYPE_ONE_SHOT
  );

  return timer;
};

const clearTimeoutXPCOM = function(timer) {
  timer.cancel();
};

const syncWaitPromise = function(promise) {
  let state, result;

  promise.then(
    val => {
      result = val;
      state = 'resolved';
    },
    err => {
      result = err;
      state = 'rejected';
    }
  );

  const thread = Services.tm.currentThread;
  while (state === undefined) {
    thread.processNextEvent(true);
  }

  if (state === 'resolved') {
    return result;
  } else if (state === 'rejected') {
    throw result;
  } else {
    throw new Error('This should not be reachable');
  }
};

const sleepNonBlocking = function(msec) {
  return syncWaitPromise(
    new Promise((resolve, reject) => {
      setTimeoutXPCOM(resolve, msec);
    })
  );
};

const sleepBlocking = function(msec) {
  const timeout = timespec();
  let rc;

  timeout.tv_sec = msec / 1000;
  timeout.tv_nsec = (msec % 1000) * 1000 * 1000;

  do {
    rc = nanosleep(timeout.address(), timeout.address());
  } while (rc === -1 && ctypes.errno === LIBC.EINTR);

  if (rc) {
    throw new Error(`Error sleeping, errno = ${ctypes.errno}`);
  }
};
