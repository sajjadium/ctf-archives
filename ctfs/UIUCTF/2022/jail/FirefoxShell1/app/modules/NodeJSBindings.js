/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */
'use strict';

// eslint-disable-next-line mozilla/no-define-cc-etc
const { CC, Cc, Cu, ChromeUtils } = require('chrome');

// eslint-disable-next-line mozilla/reject-importGlobalProperties
Cu.importGlobalProperties(['DOMException']);

/* global OS */
Cc['@mozilla.org/net/osfileconstantsservice;1'].getService(Ci.nsIOSFileConstantsService).init();

const { Services } = ChromeUtils.import('resource://gre/modules/Services.jsm');
const { ObjectUtils } = ChromeUtils.import('resource://gre/modules/ObjectUtils.jsm');

const { Stdout } = ChromeUtils.import('resource:///modules/Stdout.jsm');
const { sleepBlocking } = ChromeUtils.import('resource:///modules/Utils.jsm');

const currentGlobal = Cu.getGlobalForObject(this);

const systemPrincipal = CC('@mozilla.org/systemprincipal;1', 'nsIPrincipal')();
const debuggerSandbox = Cu.Sandbox(systemPrincipal, {
  freshCompartment: true,
});
const { addDebuggerToGlobal } = ChromeUtils.import('resource://gre/modules/jsdebugger.jsm');
addDebuggerToGlobal(debuggerSandbox);
const { Debugger } = debuggerSandbox;
const debuggerObj = new Debugger();
debuggerObj.allowUnobservedAsmJS = true;

// This should be safe considering JS's run-to-completion semantics.
// Just don't call syncWaitPromise.
let currentDebuggeeGlobal;
const setdebuggeeglobal = function(newglobal, cb) {
  const lastDebuggeeGlobal = currentDebuggeeGlobal;
  currentDebuggeeGlobal = debuggerObj.addDebuggee(newglobal || currentGlobal);

  try {
    if (cb) {
      cb();
    }
  } finally {
    if (lastDebuggeeGlobal) {
      currentDebuggeeGlobal = lastDebuggeeGlobal;
    }
  }
};

setdebuggeeglobal(null);

const debuggeeglobal = function() {
  return currentDebuggeeGlobal;
};

const debuggeeobj = function(obj) {
  try {
    return debuggeeglobal().makeDebuggeeValue(obj);
  } catch (e) {
    throw new Cu.unwaiveXrays(debuggeeglobal().unsafeDereference()).Error(e.message);
  }
};

const deref = function(obj) {
  if (typeof obj === 'object' && obj instanceof Debugger.Object) {
    return obj.unsafeDereference();
  }
  return obj;
};

const exportres = function(obj) {
  const res = ChromeUtils.shallowClone(obj, debuggeeglobal().unsafeDereference());
  if (typeof obj === 'object' && obj instanceof Array) {
    res.length = obj.length;
  }
  return res;
};

const instanceOf = function(object, type) {
  return Object.prototype.toString.call(Cu.waiveXrays(object)) === '[object ' + type + ']';
};

const XPCWrappedNative = Object.getPrototypeOf(Components);
const nsJSIID = Object.getPrototypeOf(Ci.nsISupports);

const internalBindings = {
  uiuctf: {
    ErrorCaptureStackTrace(targetObject, constructorOpt) {
      // TODO: constructorOpt not supported
      targetObject.stack = Components.stack.formattedStack;
    },

    isXPCWrappedNative(object) {
      return object instanceof Ci.nsISupports;
    },
    XPCWrappedNativeToString(object) {
      return XPCWrappedNative.toString.call(object);
    },
    isNsJSIID(object) {
      return Object.getPrototypeOf(object) === nsJSIID;
    },
    nsJSIIDToString(object) {
      return nsJSIID.toString.call(object);
    },
    // For nsJSCID name is often too long to be useful.
    // Query .name if you need it

    debugPrint(message) {
      if (typeof message !== 'string') {
        return;
      }
      Stdout.write(message);
    },
  },

  // See https://github.com/nodejs/node/tree/master/typings/internalBinding
  util: {
    // XXX: deprivileged
    // alpn_buffer_private_symbol: 0,
    // arrow_message_private_symbol: 1,
    // contextify_context_private_symbol: 2,
    // contextify_global_private_symbol: 3,
    // decorated_private_symbol: 4,
    // napi_type_tag: 5,
    // napi_wrapper: 6,
    // untransferable_object_private_symbol: 7,

    // XXX: deprivileged
    // kPending: 0,
    // kFulfilled: 1,
    // kRejected: 2,

    getHiddenValue(object, index) {},
    setHiddenValue(object, index, value) {
      return false;
    },
    // XXX: deprivileged
    // getPromiseDetails(promise: any): undefined | [state: 0] | [state: 1 | 2, result: any];
    // XXX: deprivileged
    // getProxyDetails(proxy: any, fullProxy?: boolean): undefined | any | [target: any, handler: any];
    previewEntries(object, slowPath) {
      // TODO: slowPath not supported
      if (instanceOf(object, 'WeakSet')) {
        return exportres(Array.from(ChromeUtils.nondeterministicGetWeakSetKeys(object)));
      } else if (instanceOf(object, 'WeakMap')) {
        const res = [];
        for (const key of ChromeUtils.nondeterministicGetWeakMapKeys(object)) {
          res.push(key);
          res.push(object.get(key));
        }
        return exportres(res);
      }
      return undefined;
    },
    // XXX: deprivileged
    // getOwnNonIndexProperties(object: object, filter: number): Array<string | symbol>;
    // XXX: deprivileged
    // getConstructorName(object: object): string;
    // XXX: deprivileged
    // getExternalValue(value: any): bigint;
    sleep(msec) {
      const principal = Cu.getObjectPrincipal(debuggeeglobal().unsafeDereference());
      if (!principal.isSystemPrincipal) {
        throw new Error('Permission denied');
      }

      sleepBlocking(msec);
    },
    // XXX: deprivileged
    // isConstructor(fn: Function): boolean;
    // TODO
    // arrayBufferViewHasBuffer(view: ArrayBufferView): boolean;
    // XXX: deprivileged
    // propertyFilter: {
    //   ALL_PROPERTIES: 0,
    //   ONLY_WRITABLE: 1,
    //   ONLY_ENUMERABLE: 2,
    //   ONLY_CONFIGURABLE: 4,
    //   SKIP_STRINGS: 8,
    //   SKIP_SYMBOLS: 16,
    // },
    // TODO
    // shouldAbortOnUncaughtToggle: [shouldAbort: 0 | 1],
    // XXX: deprivileged
    // WeakReference: typeof InternalUtilBinding.WeakReference;
    // guessHandleType(fd): 'TCP' | 'TTY' | 'UDP' | 'FILE' | 'PIPE' | 'UNKNOWN',
    // XXX: deprivileged
    // toUSVString(str: string, start: number): string;
  },
  types: {
    // XXX: deprivileged
    // isAsyncFunction(value: unknown): value is (...args: unknown[]) => Promise<unknown>;
    // XXX: deprivileged
    // isGeneratorFunction(value: unknown): value is GeneratorFunction;

    // Many of these aren't deprivileged because I need Xrays to make sure we
    // are looking at the right thing.
    isAnyArrayBuffer(value) {
      const global = deref(debuggeeglobal());
      return (
        value instanceof global.ArrayBuffer ||
        (global.SharedArrayBuffer && value instanceof global.SharedArrayBuffer)
      );
    },
    isArrayBuffer(value) {
      return value instanceof deref(debuggeeglobal()).ArrayBuffer;
    },
    isArgumentsObject(value) {
      return instanceOf(value, 'Arguments');
    },
    isBoxedPrimitive(value) {
      const global = deref(debuggeeglobal());
      value = Cu.waiveXrays(value);
      return (
        value instanceof Cu.waiveXrays(global.BigInt) ||
        value instanceof Cu.waiveXrays(global.Boolean) ||
        value instanceof Cu.waiveXrays(global.Number) ||
        value instanceof Cu.waiveXrays(global.String) ||
        value instanceof Cu.waiveXrays(global.Symbol)
      );
    },
    isDataView(value) {
      return value instanceof deref(debuggeeglobal()).DataView;
    },
    isExternal(value) {
      return false;
    },
    isMap(value) {
      return instanceOf(value, 'Map') && Cu.getClassName(value, true) === 'Map';
    },
    isMapIterator(value) {
      // There doesn't seem to be an XPCOM way of previewEntries for built-in
      // iterators. So just don't bother here.
      return false;
      // return instanceOf(Object.getPrototypeOf(value), 'Map Iterator');
    },
    isModuleNamespaceObject(value) {
      // TODO
      return false;
    },
    isNativeError(value) {
      return (
        debuggeeobj(value).isError ||
        value instanceof Components.Exception ||
        DOMException.isInstance(value)
      );
    },
    // XXX: deprivileged
    // isPromise: (value: unknown) => value is Promise<unknown>;
    isSet(value) {
      return instanceOf(value, 'Set') && Cu.getClassName(value, true) === 'Set';
    },
    isSetIterator(value) {
      return false;
      // return instanceOf(Object.getPrototypeOf(value), 'Set Iterator');
    },
    isWeakMap(value) {
      return (
        instanceOf(value, 'WeakMap') &&
        ChromeUtils.nondeterministicGetWeakMapKeys(value) !== undefined
      );
    },
    isWeakSet(value) {
      return (
        instanceOf(value, 'WeakSet') &&
        ChromeUtils.nondeterministicGetWeakSetKeys(value) !== undefined
      );
    },
    isRegExp(value) {
      return instanceOf(value, 'RegExp');
    },
    isDate(value) {
      return instanceOf(value, 'Date');
    },
    isTypedArray(value) {
      return instanceOf(value, 'TypedArray');
    },
    isStringObject(value) {
      return Cu.waiveXrays(value) instanceof Cu.waiveXrays(deref(debuggeeglobal()).String);
    },
    isNumberObject(value) {
      return Cu.waiveXrays(value) instanceof Cu.waiveXrays(deref(debuggeeglobal()).Number);
    },
    isBooleanObject(value) {
      return Cu.waiveXrays(value) instanceof Cu.waiveXrays(deref(debuggeeglobal()).Boolean);
    },
    isBigIntObject(value) {
      return Cu.waiveXrays(value) instanceof Cu.waiveXrays(deref(debuggeeglobal()).BigInt);
    },
  },
  constants: {
    // XXX: deprivileged completely
  },
  config: {
    // isDebugBuild: false,
    // hasOpenSSL: false,
    // fipsMode: false,
    hasIntl: false,
    // hasTracing: false,
    // hasNodeOptions: false,
    // hasInspector: false,
    noBrowserGlobals: true,
    bits: OS.Constants.Sys.bits,
    // hasDtrace: false,
  },
};

const internalBinding = function(binding, nostrict) {
  const strictify = nostrict ? i => i : ObjectUtils.strict;
  return strictify(internalBindings[binding]);
};

module.exports = {
  internalBinding,
  setdebuggeeglobal,
};
