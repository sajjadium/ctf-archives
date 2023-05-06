/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */
'use strict';

const { CC } = require('chrome');

const { Services } = require('resource://gre/modules/Services.jsm');

const { Configuration } = require('resource:///modules/Configuration.jsm');
const { inspect } = require('resource:///modules/ConsoleObserver.jsm');

const systemPrincipal = CC('@mozilla.org/systemprincipal;1', 'nsIPrincipal')();
const debuggerSandbox = Cu.Sandbox(systemPrincipal, {
  freshCompartment: true,
});
const { addDebuggerToGlobal } = require('resource://gre/modules/jsdebugger.jsm');
addDebuggerToGlobal(debuggerSandbox);
const { Debugger } = debuggerSandbox;
const debuggerObj = new Debugger();
debuggerObj.allowUnobservedAsmJS = true;

const stateMap = new WeakMap();

const deref = function(obj) {
  if (typeof obj === 'object' && obj instanceof Debugger.Object) {
    return obj.unsafeDereference();
  }
  return obj;
};

class REPL {
  constructor(getTarget, reader, writer) {
    this.getTarget = getTarget;
    this.reader = reader;
    this.writer = writer;

    this.currentStatement = '';
    this.shouldExit = false;
    this.showHidden = false;
  }

  tryHandleKeyword(line) {
    line = line.trim();
    if (!line.startsWith('.')) {
      return false;
    }

    switch (line) {
      case '.help':
        this.writer.write(`\
.break    Sometimes you get stuck, this gets you out
.clear    Alias for .break
.exit     Exit the REPL
.help     Print this help message
.show     Set console showHidden as true
.hide     Set console showHidden as false
.debug    Creates Debugger constructor on the global

Press Ctrl+C or Ctrl+D to exit the REPL
`);
        return true;
      case '.break':
      case '.clear':
        this.currentStatement = '';
        return true;
      case '.exit':
        this.shouldExit = true;
        return true;
      case '.show':
        this.showHidden = true;
        return true;
      case '.hide':
        this.showHidden = false;
        return true;
      case '.debug':
        const target = this.getTarget();
        const debuggerSandboxUnpriv = Cu.waiveXrays(
          Cu.Sandbox(target, {
            freshCompartment: true,
            wantXrays: false,
          })
        );
        addDebuggerToGlobal(debuggerSandboxUnpriv);

        const principal = Cu.getObjectPrincipal(this.getTarget());
        if (!principal.isSystemPrincipal && Configuration.hardened) {
          delete debuggerSandboxUnpriv.Debugger.prototype.addAllGlobalsAsDebuggees;
          delete debuggerSandboxUnpriv.Debugger.prototype.findAllGlobals;
          delete debuggerSandboxUnpriv.Debugger.prototype.onNewGlobalObject;
        }

        Cu.waiveXrays(target).Debugger = debuggerSandboxUnpriv.Debugger;
        return true;
      default:
        if (this.currentStatement.length) {
          return false;
        }
        this.writer.write('Invalid REPL keyword\n');
        return true;
    }
  }

  createBindings(target, debuggerGlobal, state) {
    // Make sure target is X-rayed before we potentially access the native
    // WebIDL functions in its scope.
    target = Cu.unwaiveXrays(target);

    if (state.bindingPrototype === undefined) {
      state.bindingPrototype = {
        // Browser console uses $_
        get $_() {
          return state.lastEval;
        },
        // NodeJS console uses _
        get _() {
          return state.lastEval;
        },

        // see resource://devtools/server/actors/webconsole/utils.js
        $: debuggerGlobal.makeDebuggeeValue(
          Cu.exportFunction(selector => {
            try {
              return target.document.querySelector(selector);
            } catch (err) {
              throw new target.DOMException(err.message, err.name);
            }
          }, target)
        ),

        $$: debuggerGlobal.makeDebuggeeValue(
          Cu.exportFunction(selector => {
            let nodes;
            try {
              nodes = target.document.querySelectorAll(selector);
            } catch (err) {
              throw new target.DOMException(err.message, err.name);
            }

            const result = new target.Array();
            for (let i = 0; i < nodes.length; i++) {
              result.push(nodes[i]);
            }

            return result;
          }, target)
        ),
      };
    }

    const bindings = {};

    for (const name in state.bindingPrototype) {
      if (Object.getOwnPropertyDescriptor(Cu.waiveXrays(target), name) !== undefined) {
        continue;
      }

      bindings[name] = state.bindingPrototype[name];
    }

    return bindings;
  }

  async run() {
    this.writer.write('Type ".help" for more information.\n');
    this.writer.write('Type ".debug" for Debugger. No idea what it does /shrug\n');

    while (!this.shouldExit) {
      /* ======== READ ======== */
      if (!this.currentStatement.length) {
        this.writer.write('> ');
      } else {
        this.writer.write('... ');
      }

      const line = await this.reader.readLine();
      if (!line.length) {
        return;
      } // EOF

      if (this.tryHandleKeyword(line)) {
        continue;
      }

      this.currentStatement += line;

      if (!this.currentStatement.trim().length) {
        this.currentStatement = '';
        continue;
      }

      /* ======== EVAL ======== */
      // Prefer expressions to statements. we want {a:1} to eval to an object,
      // not a code block.
      // Regex from https://github.com/nodejs/node/blob/v18.0.0/lib/repl.js#L418
      if (
        /^\s*{/.test(this.currentStatement) &&
        !/;\s*$/.test(this.currentStatement) &&
        Debugger.isCompilableUnit(`(${this.currentStatement})`)
      ) {
        this.currentStatement = `(${this.currentStatement})`;
      }
      if (!Debugger.isCompilableUnit(this.currentStatement)) {
        continue;
      }

      const target = this.getTarget();
      const debuggerGlobal = debuggerObj.makeGlobalObjectReference(target);

      // If no Xray, target is same across refreshes.
      let state = stateMap.get(Cu.waiveXrays(target));
      if (state === undefined) {
        state = {};
        stateMap.set(Cu.waiveXrays(target), state);
      }

      const bindings = this.createBindings(target, debuggerGlobal, state);

      const log = obj => inspect(obj, this.showHidden, target);
      const res = debuggerGlobal.executeInGlobalWithBindings(this.currentStatement, bindings, {
        url: 'REPL',
      });

      /* ======== PRINT ======== */
      if ('return' in res) {
        state.lastEval = res.return;
        log(deref(state.lastEval));
      }
      if ('throw' in res) {
        log(deref(res.throw));
      }

      this.currentStatement = '';
    }
  }
}

module.exports = { REPL };
