/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */
'use strict';

const EXPORTED_SYMBOLS = ['Loader'];

const { Constructor: CC, manager: Cm } = Components;
const { NetUtil } = ChromeUtils.import('resource://gre/modules/NetUtil.jsm');
const { Services } = ChromeUtils.import('resource://gre/modules/Services.jsm');
const { basename, dirname, normalize } = ChromeUtils.import(
  'resource://gre/modules/osfile/ospath_unix.jsm'
);

const bind = Function.call.bind(Function.bind);

const systemPrincipal = CC('@mozilla.org/systemprincipal;1', 'nsIPrincipal')();

const resProto = Cc['@mozilla.org/network/protocol;1?name=resource'].getService(
  Ci.nsIResProtocolHandler
);

const isAbsoluteURI = function(uri) {
  return /^(resource|chrome|file|jar):/.test(uri);
};
const isRelative = function(id) {
  return id.startsWith('.');
};

const readURI = function(uri) {
  const nsURI = NetUtil.newURI(uri);
  if (nsURI.scheme === 'resource') {
    // Resolve to a real URI, this will catch any obvious bad paths without
    // logging assertions in debug builds, see bug 1135219
    uri = resProto.resolveURI(nsURI);
  }

  const stream = NetUtil.newChannel({
    uri: NetUtil.newURI(uri, 'UTF-8'),
    loadUsingSystemPrincipal: true,
  }).open();
  const count = stream.available();
  const data = NetUtil.readInputStreamToString(stream, count, {
    charset: 'UTF-8',
  });

  stream.close();

  return data;
};

// Combines all arguments into a resolved, normalized path
const join = function(base, ...paths) {
  // If this is an absolute URL, we need to normalize only the path portion,
  // or we wind up stripping too many slashes and producing invalid URLs.
  const match = /^((?:resource|file|chrome):\/\/[^/]*|jar:[^!]+!)(.*)/.exec(base);
  if (match) {
    return match[1] + normalize([match[2], ...paths].join('/'));
  }

  return normalize([base, ...paths].join('/'));
};

// Utility function to join paths. In common case `base` is a
// `requirer.uri` but in some cases it may be `baseURI`. In order to
// avoid complexity we require `baseURI` with a trailing `/`.
const absURI = function(id, base) {
  if (!isRelative(id)) {
    return id;
  }

  const baseDir = dirname(base);

  let resolved;
  if (baseDir.includes(':')) {
    resolved = join(baseDir, id);
  } else {
    resolved = normalize(`${baseDir}/${id}`);
  }

  // Joining and normalizing removes the "./" from relative files.
  // We need to ensure the resolution still has the root
  if (base.startsWith('./')) {
    resolved = './' + resolved;
  }

  return resolved;
};

const compileMapping = function(paths) {
  // Make mapping array that is sorted from longest path to shortest path.
  const mapping = Object.keys(paths)
    .sort((a, b) => b.length - a.length)
    .map(path => [path, paths[path]]);

  const PATTERN = /([.\\?+*(){}[\]^$])/g;
  const escapeMeta = str => str.replace(PATTERN, '\\$1');

  const patterns = [];
  paths = {};

  for (let [path, uri] of mapping) {
    // Strip off any trailing slashes to make comparisons simpler
    if (path.endsWith('/')) {
      path = path.slice(0, -1);
      uri = uri.replace(/\/+$/, '');
    }

    paths[path] = uri;

    // We only want to match path segments explicitly. Examples:
    // * "foo/bar" matches for "foo/bar"
    // * "foo/bar" matches for "foo/bar/baz"
    // * "foo/bar" does not match for "foo/bar-1"
    // * "foo/bar/" does not match for "foo/bar"
    // * "foo/bar/" matches for "foo/bar/baz"
    //
    // Check for an empty path, an exact match, or a substring match
    // with the next character being a forward slash.
    if (path === '') {
      patterns.push('');
    } else {
      patterns.push(`${escapeMeta(path)}(?=$|/)`);
    }
  }

  const pattern = new RegExp(`^(${patterns.join('|')})`);

  // This will replace the longest matching path mapping at the start of
  // the ID string with its mapped value.
  return id => {
    return id.replace(pattern, (m0, m1) => paths[m1]);
  };
};

const normalizeExt = function(uri) {
  if (basename(uri).includes('.')) {
    return uri;
  }

  return uri + '.js';
};

const mapURI = function(id, mapping) {
  // Do not resolve if already a resource URI
  if (isAbsoluteURI(id)) {
    return normalizeExt(id);
  }

  return normalizeExt(mapping(id));
};

// Populates `exports` of the given CommonJS `module` object, in the context
// of the given `loader` by evaluating code associated with it.
const load = function(loader, module) {
  // We expose set of properties defined by `CommonJS` specification via
  // prototype of the sandbox. Also globals are deeper in the prototype
  // chain so that each module has access to them as well.

  const descriptors = {
    require: {
      configurable: true,
      enumerable: true,
      writable: true,
      value: module.require,
    },
    module: {
      configurable: true,
      enumerable: true,
      writable: true,
      value: module,
    },
    exports: {
      configurable: true,
      enumerable: true,
      writable: true,
      value: module.exports,
    },
  };

  // Create a new object in this sandbox, that will be used as
  // the scope object for this particular module
  const sandbox = new loader.sharedGlobalSandbox.Object();

  Object.defineProperties(sandbox, descriptors);
  loader.sandboxes[module.uri] = sandbox;

  try {
    Services.scriptloader.loadSubScript(module.uri, sandbox);
  } catch (error) {
    // loadSubScript sometime throws string errors, which includes no stack.
    // At least provide the current stack by re-throwing a real Error object.
    if (typeof error === 'string') {
      if (
        error.startsWith('Error creating URI') ||
        error.startsWith('Error opening input stream (invalid filename?)')
      ) {
        throw new Error(`Module \`${module.id}\` is not found at ${module.uri}`);
      }

      throw new Error(`Error while loading module \`${module.id}\` at ${module.uri}:\n` + error);
    }
    // Otherwise just re-throw everything else which should have a stack
    throw error;
  }

  return module;
};

const Module = function(loader, uri) {
  const module = Object.create(null, {
    exports: {
      enumerable: true,
      writable: true,
      value: Object.create(null),
      configurable: true,
    },
    id: { enumerable: true, value: uri },
    // loaded can only be visibility false for JS modules while being loaded
    loaded: { writable: true, value: true },
    require: {
      get() {
        return Require(loader, module); // eslint-disable-line no-use-before-define
      },
    },
    uri: { value: uri },
  });

  return module;
};

const EXTENSION_HANDLERS = {
  js(loader, uri) {
    // Many of the loader's functionalities are dependent
    // on loader.modules[uri] being set before loading, so we set it and
    // remove it if we have any errors.
    const module = (loader.modules[uri] = Module(loader, uri));

    module.loaded = false;

    try {
      load(loader, module);
    } catch (e) {
      // Clear out loader.modules cache so we can throw on a second invalid require
      delete loader.modules[uri];
      // Also clear out the Sandbox that was created
      delete loader.sandboxes[uri];
      throw e;
    }

    module.loaded = true;

    return module;
  },
  jsm(loader, uri) {
    const data = ChromeUtils.import(uri);
    const module = (loader.modules[uri] = Module(loader, uri));
    module.exports = data;
    return module;
  },
  json(loader, uri) {
    const data = JSON.parse(readURI(uri));
    const module = (loader.modules[uri] = Module(loader, uri));
    module.exports = data;
    return module;
  },
};

const Require = function(loader, requirer) {
  // Resolution function taking a module name/path and
  // returning a resourceURI.
  // Used by both `require` and `require.resolve`.
  const resolve = function(id) {
    if (!id) {
      throw new Error('you must provide a module name when calling require()', requirer.uri);
    }

    let uri;

    if (loader.modules[id]) {
      uri = id;
    } else if (requirer) {
      // Resolve `id` to its requirer if it's relative.
      uri = absURI(id, requirer.id);
    } else {
      uri = id;
    }

    // Resolves `uri` of module using loaders resolve function.
    if (uri) {
      if (!loader.mappingCache.has(uri)) {
        loader.mappingCache.set(uri, mapURI(uri, loader.mapping));
      }

      uri = loader.mappingCache.get(uri);
    }

    // Throw if `uri` can not be resolved.
    if (!uri) {
      throw new Error(`Module: Can not resolve '${id}' module`, requirer.uri);
    }

    return uri;
  };

  const require = function(id) {
    const uri = resolve(id);

    let module = null;
    // If module is already cached by loader then just use it.
    if (uri in loader.modules) {
      module = loader.modules[uri];
    } else {
      const base = basename(uri);
      const ext = base.slice(base.lastIndexOf('.') + 1);

      if (Object.keys(EXTENSION_HANDLERS).includes(ext)) {
        module = EXTENSION_HANDLERS[ext](loader, uri);
      } else {
        throw new Error(
          `Module: Can not handle extension '${ext}' of '${id}' module at ${uri}`,
          requirer.uri
        );
      }
    }

    return module.exports;
  };

  // Expose the `resolve` function for this `Require` instance
  require.resolve = resolve;

  // This is like webpack's require.context.  It returns a new require
  // function that prepends the prefix to any requests.
  require.context = prefix => {
    return id => {
      return require(prefix + id);
    };
  };

  Object.defineProperty(require, 'cache', {
    get() {
      return loader.modules;
    },
  });

  return require;
};

// Function makes new loader that can be used to load CommonJS modules.
// Loader takes following options:
// - `paths`: Mandatory dictionary of require path mapped to absolute URIs.
//   Object keys are path prefix used in require(), values are URIs where each
//   prefix should be mapped to.
// - `sandbox`: Sandbox used.
// The require function is returned.
const Loader = function(options) {
  const mapping = compileMapping(options.paths);
  const modules = {};
  const opts = {
    wantXrays: options.wantXrays === undefined ? true : options.wantXrays,
  };

  if (options.sandboxPrototype !== undefined) {
    opts.sandboxPrototype = options.sandboxPrototype;
  }

  const sandbox = Cu.Sandbox(systemPrincipal, opts);

  // Or else window would point to sandboxPrototype, which isn't exactly what
  // window is for...
  Object.defineProperty(sandbox, 'window', {
    value: sandbox,
    writable: false,
    enumerable: true,
    configurable: false,
  });
  Object.defineProperty(sandbox, 'global', {
    value: sandbox,
    writable: false,
    enumerable: false,
    configurable: false,
  });

  // Loader object is just a representation of a environment
  // state. We mark its properties non-enumerable
  // as they are pure implementation detail that no one should rely upon.
  const loader = Object.create(null, {
    mapping: { enumerable: false, value: mapping },
    mappingCache: { enumerable: false, value: new Map() },
    // Map of module objects indexed by module URIs.
    modules: { enumerable: false, value: modules },
    sharedGlobalSandbox: { enumerable: false, value: sandbox },
    // Map of module sandboxes indexed by module URIs.
    sandboxes: { enumerable: false, value: {} },
  });

  const builtinModuleExports = {
    loader,
    chrome: {
      Cc,
      Ci,
      Cu,
      Cr,
      Cm,
      CC: bind(CC, Components),
      components: Components,
      ChromeWorker,
      ChromeUtils,
    },
    ...options.builtinModuleExports,
  };

  for (const id of Object.keys(builtinModuleExports)) {
    // We resolve `uri` from `id` since modules are cached by `uri`.
    const uri = mapURI(id, mapping);
    const module = Module(loader, uri);

    module.exports = builtinModuleExports[id];

    modules[uri] = module;
  }

  return Require(loader, modules[mapURI('loader', mapping)]);
};
