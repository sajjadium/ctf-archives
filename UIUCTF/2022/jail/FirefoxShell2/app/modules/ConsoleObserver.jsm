/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */
'use strict';

const EXPORTED_SYMBOLS = ['init', 'inspect'];

const { Loader } = ChromeUtils.import('resource:///modules/Loader.jsm');
const { Services } = ChromeUtils.import('resource://gre/modules/Services.jsm');
const { addDebuggerToGlobal } = ChromeUtils.import('resource://gre/modules/jsdebugger.jsm');

const { Stdout } = ChromeUtils.import('resource:///modules/Stdout.jsm');
const { fallbackLogExc, setTimeoutXPCOM, syncWaitPromise } = ChromeUtils.import(
  'resource:///modules/Utils.jsm'
);

const nullPrincipal = Services.scriptSecurityManager.createNullPrincipal({});

const currentGlobal = Cu.getGlobalForObject(this);
const nullSandbox = Cu.Sandbox(nullPrincipal);

const binding_require = Loader({
  paths: {
    chrome: 'resource://gre/@chrome',
  },
});

const { internalBinding, setdebuggeeglobal } = binding_require(
  'resource:///modules/NodeJSBindings.js'
);

const globalFromWindowID = function(windowID) {
  if (typeof windowID !== 'number') {
    return undefined;
  }

  const windowFromWM = Services.wm.getOuterWindowWithId(windowID);
  if (windowFromWM) {
    return windowFromWM;
  }

  return undefined;
};

const webpackCompiled = syncWaitPromise(ChromeUtils.compileScript('resource:///nodejs-bundled.js'));

// I made sure to make it as secure as possible by putting the bulk of the
// pretty printer stack into the same compartment as the global. Good luck!
const webpackEval = function(assumeGlobal) {
  const trampoline = function(execfunc) {
    const sandbox = Cu.Sandbox(Cu.getObjectPrincipal(assumeGlobal), {
      wantXrays: false,
      freshZone: true,
    });

    try {
      addDebuggerToGlobal(Cu.waiveXrays(sandbox));
      sandbox.assumeGlobal = assumeGlobal;
      sandbox.internalBinding = Cu.exportFunction(binding => {
        return Cu.cloneInto(internalBinding(binding, true), sandbox, {
          cloneFunctions: true,
        });
      }, sandbox);

      webpackCompiled.executeInGlobal(sandbox);

      const result = execfunc(sandbox);
      if (typeof result !== 'string') {
        throw new Error('Invalid format');
      }

      return result;
    } finally {
      setTimeoutXPCOM(() => {
        try {
          Cu.nukeSandbox(Cu.unwaiveXrays(sandbox));
        } catch (e) {}
      }, 0);
    }
  };

  return {
    // No idea why sandbox.inspect is x-rayed but it is
    formatWithOptions(inspectOptions, ...args) {
      const execfunc = sandbox => {
        return Cu.waiveXrays(sandbox.inspect).formatWithOptions(
          Cu.cloneInto(inspectOptions, sandbox),
          ...args
        );
      };
      return trampoline(execfunc);
    },
    inspect(value, opts) {
      const execfunc = sandbox => {
        return Cu.waiveXrays(sandbox.inspect).inspect(value, Cu.cloneInto(opts, sandbox));
      };
      return trampoline(execfunc);
    },
  };
};

const formatToStdout = function(assumeGlobal, doInspect, showHidden, ...args) {
  const principal = Cu.getObjectPrincipal(assumeGlobal);

  if (!principal.isSystemPrincipal) {
    args = Array.from(args).map(arg => Cu.waiveXrays(arg));
  }

  setdebuggeeglobal(assumeGlobal, () => {
    try {
      const inspectModule = webpackEval(assumeGlobal);
      const opts = {
        colors: true,
        showProxy: true,
        customInspect: false,
        showHidden,
      };

      if (doInspect) {
        Stdout.write(`${inspectModule.inspect(args[0], opts)}\n`);
      } else {
        Stdout.write(`${inspectModule.formatWithOptions(opts, ...args)}\n`);
      }
    } catch (e) {
      fallbackLogExc(e);
    }
  });
};

const inspect = function(obj, showHidden = true, assumeGlobal = undefined) {
  if (assumeGlobal === undefined) {
    assumeGlobal = currentGlobal;
  }
  formatToStdout(assumeGlobal, true, showHidden, obj);
};

const ConsoleObserver = {
  QueryInterface: ChromeUtils.generateQI([Ci.nsIObserver]),

  init() {
    Services.obs.addObserver(this, 'console-api-log-event');
  },

  observe(subject, topic, data) {
    if (topic !== 'console-api-log-event') {
      return;
    }

    const consoleEvent = subject.wrappedJSObject;

    let args = consoleEvent.arguments;
    if (!Array.isArray(args)) {
      args = Array.prototype.slice.call(args);
    }

    let assumeGlobal = globalFromWindowID(consoleEvent.ID);
    if (!assumeGlobal) {
      if (consoleEvent.chromeContext) {
        assumeGlobal = currentGlobal;
      } else {
        assumeGlobal = nullSandbox;
      }
    }

    const doErrorMsg = obj => {
      switch (obj.error) {
        case 'counterDoesntExist':
          args = [`Counter "${obj.label}" doesn't exist`];
          return true;
        case 'maxTimersExceeded':
          args = ['The maximum allowed number of timers was exceeded'];
          return true;
        case 'timerAlreadyExists':
          args = [`Timer "${obj.name}" already exists`];
          return true;
        case 'timerDoesntExist':
          args = [`Timer "${obj.name}" doesn't exist`];
          return true;
        case 'timerJSError':
          args = ['Failed to process the timer name.'];
          return true;
        default:
          // Don't know how to handle
          return false;
      }
    };
    let doInspect = false;
    let showHidden = false;
    switch (consoleEvent.level) {
      case 'debug':
      case 'error':
      case 'info':
      case 'log':
      case 'warn':
        break;
      case 'assert':
        args = ['Assertion failed:', ...args];
        break;
      case 'clear':
        Stdout.write('\x1b[2J\x1b[H');
        return;
      case 'count':
        args = [`${consoleEvent.counter.label}: ${consoleEvent.counter.count}`];
        break;
      case 'countReset':
        if (consoleEvent.counter.error) {
          if (!doErrorMsg(consoleEvent.counter)) {
            return;
          }
        } else {
          args = [`${consoleEvent.counter.label}: ${consoleEvent.counter.count}`];
        }
        break;
      case 'dir':
      case 'dirxml':
        args = [args[0]];
        doInspect = true;
        showHidden = true;
        break;
      case 'group':
      case 'groupCollapsed':
      case 'groupEnd':
        // TODO
        return;
      case 'table':
        // TODO
        return;
      case 'time':
        if (consoleEvent.timer.error) {
          if (!doErrorMsg(consoleEvent.timer)) {
            return;
          }
        }

        // Nothing to do
        return;
      case 'timeLog':
      case 'timeEnd':
        if (consoleEvent.timer.error) {
          if (!doErrorMsg(consoleEvent.timer)) {
            return;
          }
        } else {
          args = [
            `${consoleEvent.timer.name}: ${(consoleEvent.timer.duration / 1000).toFixed(3)}s`,
          ];
        }
        break;
      case 'trace':
        // This is kinda insane, but the least insane thing we can do here is
        // Print out all the objects, then create a stack trace with an error.
        formatToStdout(assumeGlobal, false, false, 'console.trace()', ...args);

        const ctor = Cu.unwaiveXrays(assumeGlobal).Error;
        const exception = Cu.waiveXrays(new ctor());

        exception.name = 'Trace:';

        // Need to generate the stack trace manually because the stack contains
        // traces from here. :(
        // ... or not. unprivileged mode doesn't get it.
        // exception.stack = '';
        // for (const entry of consoleEvent.stacktrace)
        //   exception.stack += `${entry.functionName}@${entry.filename}:${entry.lineNumber}:${entry.columnNumber}\n`;
        // Object.defineProperty(exception, 'stack', {
        //   value: exception.stack,
        //   enumerable: false,
        // });

        formatToStdout(assumeGlobal, false, false, exception);
        return;
    }

    formatToStdout(assumeGlobal, doInspect, showHidden, ...args);
  },
};

const ConsoleListener = {
  QueryInterface: ChromeUtils.generateQI([Ci.nsIConsoleListener]),

  init() {
    Services.console.registerListener(this);
  },

  observe(message) {
    if (!(message instanceof Ci.nsIScriptError)) {
      return;
    }

    message = message.QueryInterface(Ci.nsIScriptError);

    let assumeGlobal = globalFromWindowID(message.outerWindowID);
    if (!assumeGlobal) {
      if (message.isFromChromeContext) {
        assumeGlobal = currentGlobal;
      } else {
        assumeGlobal = nullSandbox;
      }
    }

    let exception = message.exception;
    if (!message.hasException) {
      if (message.stack || message.isFromChromeContext) {
        exception = Cu.waiveXrays(ChromeUtils.createError(message.errorMessage, message.stack));
        exception.name = '';
      } else {
        const ctor = Cu.unwaiveXrays(assumeGlobal).Error;
        exception = Cu.waiveXrays(new ctor(message.errorMessage));
        exception.name = '';
        delete exception.stack;
      }
    }

    const prefix =
      message.flags & Ci.nsIScriptError.warningFlag ? 'Warning:' : 'Uncaught Exception:';

    formatToStdout(assumeGlobal, false, false, prefix, exception);
  },
};

const init = function() {
  ConsoleObserver.init();
  ConsoleListener.init();
};
