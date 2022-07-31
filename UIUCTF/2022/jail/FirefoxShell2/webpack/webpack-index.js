/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */
'use strict';

const { ErrorCaptureStackTrace, debugPrint, getDebugger } = globalThis.internalBinding('uiuctf');
const { previewEntries } = globalThis.internalBinding('util');

const Debugger = globalThis.Debugger;

globalThis.primordials = { ErrorCaptureStackTrace };
globalThis.process = { platform: 'linux', versions: {} };

require('internal/per_context/primordials');

const debuggeeglobal = (function(assumeGlobal) {
  let currentDebuggeeGlobal;

  return function() {
    if (currentDebuggeeGlobal === undefined) {
      const debuggerObj = new Debugger();
      debuggerObj.allowUnobservedAsmJS = true;
      currentDebuggeeGlobal = debuggerObj.addDebuggee(assumeGlobal);
    }

    return currentDebuggeeGlobal;
  };
})(globalThis.assumeGlobal);

const debuggeeobj = function(obj) {
  return debuggeeglobal().makeDebuggeeValue(obj);
};

const deref = function(obj) {
  if (typeof obj === 'object' && obj instanceof Debugger.Object) {
    return obj.unsafeDereference();
  }
  return obj;
};

const exportres = function(obj) {
  return obj;
};

const instanceOf = function(object, type) {
  return Object.prototype.toString.call(object) === '[object ' + type + ']';
};

const deprivilegedBindings = {
  util: {
    alpn_buffer_private_symbol: 0,
    arrow_message_private_symbol: 1,
    contextify_context_private_symbol: 2,
    contextify_global_private_symbol: 3,
    decorated_private_symbol: 4,
    napi_type_tag: 5,
    napi_wrapper: 6,
    untransferable_object_private_symbol: 7,

    kPending: 0,
    kFulfilled: 1,
    kRejected: 2,

    getPromiseDetails(promise) {
      const target = debuggeeobj(promise);
      if (!target.isPromise) {
        return undefined;
      }

      switch (target.promiseState) {
        case 'pending':
          return exportres([deprivilegedBindings.util.kPending]);
        case 'fulfilled':
          return exportres([deprivilegedBindings.util.kFulfilled, deref(target.promiseValue)]);
        case 'rejected':
          return exportres([deprivilegedBindings.util.kRejected, deref(target.promiseReason)]);
      }

      return undefined;
    },
    getProxyDetails(proxy, fullProxy) {
      const target = debuggeeobj(proxy);
      if (!target.isProxy) {
        return undefined;
      }

      if (!fullProxy) {
        return deref(target.proxyTarget);
      }
      return exportres([deref(target.proxyTarget), deref(target.proxyHandler)]);
    },
    previewEntries(object, slowPath) {
      const origres = previewEntries(object, slowPath);
      if (!origres) {
        return origres;
      }
      return Array.from(origres);
    },
    getOwnNonIndexProperties(object, filter) {
      const ret = [];

      if (!(filter & deprivilegedBindings.util.propertyFilter.SKIP_STRINGS)) {
        for (const prop in Object.getOwnPropertyNames(object)) {
          // https://stackoverflow.com/a/38163613
          if ((prop >>> 0) + '' === prop && prop < 4294967295) {
            continue;
          }

          const desc = Object.getOwnPropertyDescriptor(object, prop);

          if (filter & deprivilegedBindings.util.propertyFilter.ONLY_WRITABLE && !desc.writable) {
            continue;
          }
          if (
            filter & deprivilegedBindings.util.propertyFilter.ONLY_ENUMERABLE &&
            !desc.enumerable
          ) {
            continue;
          }
          if (
            filter & deprivilegedBindings.util.propertyFilter.ONLY_CONFIGURABLE &&
            !desc.configurable
          ) {
            continue;
          }

          ret.push(prop);
        }
      }

      if (!(filter & deprivilegedBindings.util.propertyFilter.SKIP_SYMBOLS)) {
        for (const prop in Object.getOwnPropertySymbols(object)) {
          const desc = Object.getOwnPropertyDescriptor(object, prop);

          if (filter & deprivilegedBindings.util.propertyFilter.ONLY_WRITABLE && !desc.writable) {
            continue;
          }
          if (
            filter & deprivilegedBindings.util.propertyFilter.ONLY_ENUMERABLE &&
            !desc.enumerable
          ) {
            continue;
          }
          if (
            filter & deprivilegedBindings.util.propertyFilter.ONLY_CONFIGURABLE &&
            !desc.configurable
          ) {
            continue;
          }

          ret.push(prop);
        }
      }

      return ret;
    },
    getConstructorName(object) {
      return debuggeeobj(object).class;
    },
    getExternalValue(value) {
      throw new Error('Not supported');
    },
    isConstructor(fn) {
      return debuggeeobj(fn).isClassConstructor;
    },
    propertyFilter: {
      ALL_PROPERTIES: 0,
      ONLY_WRITABLE: 1,
      ONLY_ENUMERABLE: 2,
      ONLY_CONFIGURABLE: 4,
      SKIP_STRINGS: 8,
      SKIP_SYMBOLS: 16,
    },
    WeakReference: WeakRef,
    toUSVString(str, start) {
      // source: browser/chrome/devtools/modules/devtools/client/shared/vendor/whatwg-url.js
      const S = String(str);
      const n = S.length;
      const U = [];
      for (let i = 0; i < n; ++i) {
        const c = S.charCodeAt(i);
        if (c < 0xd800 || c > 0xdfff) {
          U.push(String.fromCodePoint(c));
        } else if (0xdc00 <= c && c <= 0xdfff) {
          U.push(String.fromCodePoint(0xfffd));
        } else if (i === n - 1) {
          U.push(String.fromCodePoint(0xfffd));
        } else {
          const d = S.charCodeAt(i + 1);
          if (0xdc00 <= d && d <= 0xdfff) {
            const a = c & 0x3ff;
            const b = d & 0x3ff;
            U.push(String.fromCodePoint((2 << 15) + (2 << 9) * a + b));
            ++i;
          } else {
            U.push(String.fromCodePoint(0xfffd));
          }
        }
      }

      return U.join('');
    },
  },
  types: {
    isAsyncFunction(value) {
      return debuggeeobj(value).isAsyncFunction;
    },
    isGeneratorFunction(value) {
      return debuggeeobj(value).isGeneratorFunction;
    },

    isPromise(value) {
      return debuggeeobj(value).isPromise;
    },
  },
  constants: {
    os: {
      errno: {
        E2BIG: 7,
        EACCES: 13,
        EADDRINUSE: 48,
        EADDRNOTAVAIL: 49,
        EAFNOSUPPORT: 47,
        EAGAIN: 35,
        EALREADY: 37,
        EBADF: 9,
        EBADMSG: 94,
        EBUSY: 16,
        ECANCELED: 89,
        ECHILD: 10,
        ECONNABORTED: 53,
        ECONNREFUSED: 61,
        ECONNRESET: 54,
        EDEADLK: 11,
        EDESTADDRREQ: 39,
        EDOM: 33,
        EDQUOT: 69,
        EEXIST: 17,
        EFAULT: 14,
        EFBIG: 27,
        EHOSTUNREACH: 65,
        EIDRM: 90,
        EILSEQ: 92,
        EINPROGRESS: 36,
        EINTR: 4,
        EINVAL: 22,
        EIO: 5,
        EISCONN: 56,
        EISDIR: 21,
        ELOOP: 62,
        EMFILE: 24,
        EMLINK: 31,
        EMSGSIZE: 40,
        EMULTIHOP: 95,
        ENAMETOOLONG: 63,
        ENETDOWN: 50,
        ENETRESET: 52,
        ENETUNREACH: 51,
        ENFILE: 23,
        ENOBUFS: 55,
        ENODATA: 96,
        ENODEV: 19,
        ENOENT: 2,
        ENOEXEC: 8,
        ENOLCK: 77,
        ENOLINK: 97,
        ENOMEM: 12,
        ENOMSG: 91,
        ENOPROTOOPT: 42,
        ENOSPC: 28,
        ENOSR: 98,
        ENOSTR: 99,
        ENOSYS: 78,
        ENOTCONN: 57,
        ENOTDIR: 20,
        ENOTEMPTY: 66,
        ENOTSOCK: 38,
        ENOTSUP: 45,
        ENOTTY: 25,
        ENXIO: 6,
        EOPNOTSUPP: 102,
        EOVERFLOW: 84,
        EPERM: 1,
        EPIPE: 32,
        EPROTO: 100,
        EPROTONOSUPPORT: 43,
        EPROTOTYPE: 41,
        ERANGE: 34,
        EROFS: 30,
        ESPIPE: 29,
        ESRCH: 3,
        ESTALE: 70,
        ETIME: 101,
        ETIMEDOUT: 60,
        ETXTBSY: 26,
        EWOULDBLOCK: 35,
        EXDEV: 18,
      },
      signals: {
        SIGHUP: 1,
        SIGINT: 2,
        SIGQUIT: 3,
        SIGILL: 4,
        SIGTRAP: 5,
        SIGABRT: 6,
        SIGIOT: 6,
        SIGBUS: 10,
        SIGFPE: 8,
        SIGKILL: 9,
        SIGUSR1: 30,
        SIGSEGV: 11,
        SIGUSR2: 31,
        SIGPIPE: 13,
        SIGALRM: 14,
        SIGTERM: 15,
        SIGCHLD: 20,
        SIGCONT: 19,
        SIGSTOP: 17,
        SIGTSTP: 18,
        SIGTTIN: 21,
        SIGTTOU: 22,
        SIGURG: 16,
        SIGXCPU: 24,
        SIGXFSZ: 25,
        SIGVTALRM: 26,
        SIGPROF: 27,
        SIGWINCH: 28,
        SIGIO: 23,
        SIGINFO: 29,
        SIGSYS: 12,
      },
    },
    fs: {
      O_RDONLY: 0,
      O_WRONLY: 1,
      O_RDWR: 2,
      S_IFMT: 61440,
      S_IFREG: 32768,
      S_IFDIR: 16384,
      S_IFCHR: 8192,
      S_IFBLK: 24576,
      S_IFIFO: 4096,
      S_IFLNK: 40960,
      S_IFSOCK: 49152,
      O_CREAT: 512,
      O_EXCL: 2048,
      O_NOCTTY: 131072,
      O_TRUNC: 1024,
      O_APPEND: 8,
      O_DIRECTORY: 1048576,
      O_NOFOLLOW: 256,
      O_SYNC: 128,
      O_DSYNC: 4194304,
      O_SYMLINK: 2097152,
      O_NONBLOCK: 4,
      S_IRWXU: 448,
      S_IRUSR: 256,
      S_IWUSR: 128,
      S_IXUSR: 64,
      S_IRWXG: 56,
      S_IRGRP: 32,
      S_IWGRP: 16,
      S_IXGRP: 8,
      S_IRWXO: 7,
      S_IROTH: 4,
      S_IWOTH: 2,
      S_IXOTH: 1,
      F_OK: 0,
      R_OK: 4,
      W_OK: 2,
      X_OK: 1,
    },
  },
};

globalThis.internalBinding = (function(orig) {
  return function internalBinding(binding) {
    const origres = orig(binding);

    if (binding in deprivilegedBindings) {
      return Object.assign(origres, deprivilegedBindings[binding]);
    }

    return origres;
  };
})(globalThis.internalBinding);

globalThis.inspect = require('internal/util/inspect');

delete globalThis.Debugger;
delete globalThis.internalBinding;
