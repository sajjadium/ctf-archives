(function(){
    "use strict";
    if (typeof SNOW === "function") return;
    /******/ (() => { // webpackBootstrap
    /******/ 	var __webpack_modules__ = ({
    
    /***/ 586:
    /***/ ((module, __unused_webpack_exports, __webpack_require__) => {
    
    const hook = __webpack_require__(228);
    const {
      getFramesArray,
      getFrameTag
    } = __webpack_require__(648);
    const {
      getOnload,
      setOnload,
      removeAttribute,
      addEventListener
    } = __webpack_require__(14);
    function resetOnloadAttribute(frame) {
      if (!getFrameTag(frame)) {
        return;
      }
      addEventListener(frame, 'load', function () {
        hook(frame);
      });
      const onload = getOnload(frame);
      if (onload) {
        setOnload(frame, null);
        removeAttribute(frame, 'onload');
        setOnload(frame, onload);
      }
    }
    function resetOnloadAttributes(args) {
      for (let i = 0; i < args.length; i++) {
        const element = args[i];
        const frames = getFramesArray(element, true);
        for (let i = 0; i < frames.length; i++) {
          const frame = frames[i];
          resetOnloadAttribute(frame);
        }
      }
    }
    module.exports = resetOnloadAttributes;
    
    /***/ }),
    
    /***/ 750:
    /***/ ((module, __unused_webpack_exports, __webpack_require__) => {
    
    /*
    
    This crazy function is a workaround to support 'object' in this project
    in chromium due to a bug that can be reproduced by running:
    
    <script>
        document.body.innerHTML = ('<object id="wow" data="/" />');
        alert(window[0]); // undefined
        wow.contentWindow.frameElement;
        alert(window[0]); // [object Window]
    </script>
    
    Seems that in order for the object frame to appear in window.frames,
    one must first try to access any property of it.
    
    This for some reason registers it to the window.frames list, otherwise it won't be there.
    
    UPDATE: doesn't have to be a direct prop access, could also be a less
    vulnerable and less direct manipulation (see https://github.com/LavaMoat/snow/issues/98)
    
    */
    
    const {
      Object
    } = __webpack_require__(14);
    function workaroundChromiumBug(frame) {
      frame && Object.getOwnPropertyDescriptor(frame, '');
    }
    module.exports = workaroundChromiumBug;
    
    /***/ }),
    
    /***/ 407:
    /***/ ((module) => {
    
    const getLength = Object.getOwnPropertyDescriptor(window, 'length').get;
    const getLengthTop = getLength.bind(window);
    const createElement = Object.getOwnPropertyDescriptor(Document.prototype, 'createElement').value.bind(document);
    const appendChild = Object.getOwnPropertyDescriptor(Node.prototype, 'appendChild').value.bind(document.documentElement);
    const removeChild = Object.getOwnPropertyDescriptor(Node.prototype, 'removeChild').value.bind(document.documentElement);
    function runInNewRealm(cb) {
      const length = getLengthTop();
      const ifr = createElement('IFRAME');
      appendChild(ifr);
      const ret = cb(window[length]);
      removeChild(ifr);
      return ret;
    }
    module.exports = {
      getLength,
      runInNewRealm
    };
    
    /***/ }),
    
    /***/ 832:
    /***/ ((module, __unused_webpack_exports, __webpack_require__) => {
    
    const {
      Object,
      Function
    } = __webpack_require__(14);
    const {
      isTagFramable
    } = __webpack_require__(648);
    const {
      error,
      ERR_EXTENDING_FRAMABLES_BLOCKED
    } = __webpack_require__(312);
    function getHook(win, native) {
      return function (name, constructor, options) {
        let opts = options;
        if (options) {
          const extend = options.extends;
          if (isTagFramable(extend + '')) {
            throw error(ERR_EXTENDING_FRAMABLES_BLOCKED, name, options);
          }
        }
        return Function.prototype.call.call(native, this, name, constructor, opts);
      };
    }
    function hookCustoms(win) {
      const desc = Object.getOwnPropertyDescriptor(win.CustomElementRegistry.prototype, 'define');
      desc.configurable = desc.writable = true;
      const val = desc.value;
      desc.value = getHook(win, val);
      Object.defineProperty(win.CustomElementRegistry.prototype, 'define', desc);
    }
    module.exports = hookCustoms;
    
    /***/ }),
    
    /***/ 228:
    /***/ ((module, __unused_webpack_exports, __webpack_require__) => {
    
    const workaroundChromiumBug = __webpack_require__(750);
    const {
      getLength
    } = __webpack_require__(407);
    const {
      shadows,
      toArray,
      getFramesArray,
      getContentWindowOfFrame,
      getOwnerWindowOfNode
    } = __webpack_require__(648);
    const {
      Object,
      getFrameElement,
      Function
    } = __webpack_require__(14);
    const {
      forEachOpened
    } = __webpack_require__(134);
    function isCrossOrigin(dst, src) {
      return Object.getPrototypeOf.call(src, dst) === null;
    }
    function findWin(win, frameElement) {
      const length = Function.prototype.call.call(getLength, win);
      for (let i = 0; i < length; i++) {
        if (isCrossOrigin(win[i], win)) {
          continue;
        }
        if (getFrameElement(win[i]) === frameElement) {
          return win[i];
        }
        const found = findWin(win[i], frameElement);
        if (found) {
          return found;
        }
      }
      for (let i = 0; i < shadows.length; i++) {
        const shadow = shadows[i];
        const owner = getOwnerWindowOfNode(shadow);
        if (owner !== win) {
          continue;
        }
        const frames = getFramesArray(shadow, false);
        for (let j = 0; j < frames.length; j++) {
          const frame = frames[j];
          const win = getContentWindowOfFrame(frame);
          if (frame === frameElement) {
            return win;
          }
          const found = findWin(win, frameElement);
          if (found) {
            return found;
          }
        }
      }
      return null;
    }
    function hookWin(win) {
      top['SNOW_WINDOW'](win);
    }
    function findAndHookWin(win, frame) {
      const contentWindow = findWin(win, frame);
      if (contentWindow) {
        hookWin(contentWindow);
      }
      return !!contentWindow;
    }
    function hook(frames) {
      frames = toArray(frames);
      for (let i = 0; i < frames.length; i++) {
        const frame = frames[i];
        if (typeof frame === 'object' && frame !== null) {
          workaroundChromiumBug(frame);
          findAndHookWin(top, frame) || forEachOpened(findAndHookWin, frame);
        }
      }
    }
    module.exports = hook;
    
    /***/ }),
    
    /***/ 328:
    /***/ ((module, __unused_webpack_exports, __webpack_require__) => {
    
    const {
      getFramesArray,
      getDeclarativeShadows
    } = __webpack_require__(648);
    const {
      document,
      getChildElementCount,
      setInnerHTML
    } = __webpack_require__(14);
    const {
      error,
      ERR_DECLARATIVE_SHADOWS_BLOCKED,
      ERR_HTML_FRAMES_SRCDOC_BLOCKED
    } = __webpack_require__(312);
    function assertHTML(args) {
      for (let i = 0; i < args.length; i++) {
        const template = document.createElement('html');
        setInnerHTML(template, args[i]);
        if (getChildElementCount(template)) {
          if (getDeclarativeShadows(template).length > 0) {
            throw error(ERR_DECLARATIVE_SHADOWS_BLOCKED, args[i]);
          }
          const frames = getFramesArray(template, false);
          for (let j = 0; j < frames.length; j++) {
            const frame = frames[j];
            if (template.getAttribute.call(frame, 'srcdoc')) {
              throw error(ERR_HTML_FRAMES_SRCDOC_BLOCKED, args[i]);
            }
          }
        }
      }
    }
    module.exports = {
      assertHTML
    };
    
    /***/ }),
    
    /***/ 352:
    /***/ ((module, __unused_webpack_exports, __webpack_require__) => {
    
    const hook = __webpack_require__(228);
    const hookCreateObjectURL = __webpack_require__(716);
    const hookCustoms = __webpack_require__(832);
    const hookOpen = __webpack_require__(583);
    const hookRequest = __webpack_require__(278);
    const hookEventListenersSetters = __webpack_require__(459);
    const hookDOMInserters = __webpack_require__(58);
    const hookWorker = __webpack_require__(744);
    const hookTrustedHTMLs = __webpack_require__(294);
    const {
      hookShadowDOM
    } = __webpack_require__(373);
    const {
      Array,
      push,
      addEventListener,
      getFrameElement
    } = __webpack_require__(14);
    const {
      makeDescriptorSetter
    } = __webpack_require__(648);
    const {
      isMarked,
      mark
    } = __webpack_require__(111);
    const {
      error,
      ERR_CB_MUST_BE_FUNCTION,
      ERR_MARK_NEW_WINDOW_FAILED
    } = __webpack_require__(312);
    const setSnowWindowUtil = makeDescriptorSetter('SNOW_WINDOW', function (win) {
      onWin(win);
    });
    const setSnowFrameUtil = makeDescriptorSetter('SNOW_FRAME', function (frame) {
      hook(frame);
    });
    const setSnowUtil = makeDescriptorSetter('SNOW', snow);
    function shouldHook(win) {
      try {
        const run = !isMarked(win);
        if (run) {
          mark(win);
        }
        return run;
      } catch (err) {
        error(ERR_MARK_NEW_WINDOW_FAILED, win, err);
      }
      return shouldHook(win);
    }
    function onLoad(win) {
      const frame = getFrameElement(win);
      const onload = function () {
        hook(frame);
      };
      addEventListener(frame, 'load', onload);
    }
    function applyHooks(win) {
      setSnowUtil(win);
      onLoad(win);
      hookCreateObjectURL(win);
      hookCustoms(win);
      hookOpen(win);
      hookRequest(win);
      hookEventListenersSetters(win, 'load');
      hookDOMInserters(win);
      hookShadowDOM(win);
      hookTrustedHTMLs(win);
      hookWorker(win);
    }
    function onWin(win, cb, skip) {
      if (!skip && shouldHook(win)) {
        applyHooks(win);
        for (let i = 0; i < callbacks.length; i++) {
          const stop = callbacks[i](win);
          if (stop) {
            return;
          }
        }
      }
      if (cb) {
        cb(win);
      }
    }
    const callbacks = new Array();
    function snow(cb, win) {
      if (typeof cb !== 'function') {
        const bail = error(ERR_CB_MUST_BE_FUNCTION, cb);
        if (bail) {
          return;
        }
      }
      setSnowWindowUtil(top);
      setSnowFrameUtil(top);
      const first = push(callbacks, cb) === 1;
      const w = win || window;
      onWin(w, cb, !first && w === top);
    }
    module.exports = snow;
    
    /***/ }),
    
    /***/ 58:
    /***/ ((module, __unused_webpack_exports, __webpack_require__) => {
    
    const {
      error,
      ERR_NON_TOP_DOCUMENT_WRITE_BLOCKED
    } = __webpack_require__(312);
    const {
      protectShadows
    } = __webpack_require__(373);
    const resetOnloadAttributes = __webpack_require__(586);
    const {
      getFramesArray,
      shadows
    } = __webpack_require__(648);
    const {
      getParentElement,
      getCommonAncestorContainer,
      slice,
      Object,
      Function
    } = __webpack_require__(14);
    const {
      assertHTML
    } = __webpack_require__(328);
    const hook = __webpack_require__(228);
    const map = {
      Range: ['insertNode'],
      DocumentFragment: ['replaceChildren', 'append', 'prepend'],
      Document: ['replaceChildren', 'append', 'prepend', 'write', 'writeln'],
      Node: ['appendChild', 'insertBefore', 'replaceChild'],
      Element: ['innerHTML', 'outerHTML', 'insertAdjacentHTML', 'replaceWith', 'insertAdjacentElement', 'append', 'before', 'prepend', 'after', 'replaceChildren'],
      ShadowRoot: ['innerHTML'],
      HTMLIFrameElement: ['srcdoc']
    };
    const protos = Object.getOwnPropertyNames(map);
    function getHook(native, isRange, isWrite) {
      function before(args) {
        resetOnloadAttributes(args);
        resetOnloadAttributes(shadows);
        assertHTML(args);
      }
      function after(args, element) {
        const frames = getFramesArray(element, false);
        hook(frames);
        hook(args);
        protectShadows(true);
      }
      return function () {
        if (isWrite && this !== top.document) {
          throw error(ERR_NON_TOP_DOCUMENT_WRITE_BLOCKED, this);
        }
        const args = slice(arguments);
        const element = isRange ? getCommonAncestorContainer(this) : getParentElement(this) || this;
        before(args);
        const ret = Function.prototype.apply.call(native, this, args);
        after(args, element);
        return ret;
      };
    }
    function hookDOMInserters(win) {
      for (let i = 0; i < protos.length; i++) {
        const proto = protos[i];
        const funcs = map[proto];
        for (let i = 0; i < funcs.length; i++) {
          const func = funcs[i];
          const desc = Object.getOwnPropertyDescriptor(win[proto].prototype, func);
          if (!desc) continue;
          const prop = desc.set ? 'set' : 'value';
          const isRange = proto === 'Range',
            isWrite = func === 'write' || func === 'writeln';
          desc[prop] = getHook(desc[prop], isRange, isWrite);
          desc.configurable = true;
          if (prop === 'value') {
            desc.writable = true;
          }
          Object.defineProperty(win[proto].prototype, func, desc);
        }
      }
    }
    module.exports = hookDOMInserters;
    
    /***/ }),
    
    /***/ 459:
    /***/ ((module, __unused_webpack_exports, __webpack_require__) => {
    
    const hook = __webpack_require__(228);
    const {
      removeEventListener,
      addEventListener,
      slice,
      Map,
      Object
    } = __webpack_require__(14);
    const handlers = new Map();
    function fire(that, listener, args) {
      if (listener) {
        if (listener.handleEvent) {
          return listener.handleEvent.apply(listener, args);
        } else {
          return listener.apply(that, args);
        }
      }
    }
    function getAddEventListener(win, event) {
      return function (type, handler, options) {
        let listener = handler;
        if (type === event) {
          if (!handlers.has(handler)) {
            handlers.set(handler, function () {
              hook(this);
              const args = slice(arguments);
              fire(this, handler, args);
            });
          }
          listener = handlers.get(handler);
        }
        return addEventListener(this || win, type, listener, options);
      };
    }
    function getRemoveEventListener(win, event) {
      return function (type, handler, options) {
        let listener = handler;
        if (type === event) {
          listener = handlers.get(handler);
          handlers.delete(handler);
        }
        return removeEventListener(this || win, type, listener, options);
      };
    }
    function hookEventListenersSetters(win, event) {
      Object.defineProperty(win.EventTarget.prototype, 'addEventListener', {
        configurable: true,
        writable: true,
        value: getAddEventListener(win, event)
      });
      Object.defineProperty(win.EventTarget.prototype, 'removeEventListener', {
        configurable: true,
        writable: true,
        value: getRemoveEventListener(win, event)
      });
    }
    module.exports = hookEventListenersSetters;
    
    /***/ }),
    
    /***/ 312:
    /***/ ((module) => {
    
    const ERR_MARK_NEW_WINDOW_FAILED = 1;
    const ERR_CB_MUST_BE_FUNCTION = 2;
    const ERR_OPEN_JS_SCHEME_BLOCKED = 3;
    const ERR_OPENED_PROP_ACCESS_BLOCKED = 4;
    const ERR_DECLARATIVE_SHADOWS_BLOCKED = 5;
    const ERR_EXTENDING_FRAMABLES_BLOCKED = 6;
    const ERR_BLOB_TYPE_BLOCKED = 7;
    const ERR_HTML_FRAMES_SRCDOC_BLOCKED = 8;
    const ERR_NON_TOP_DOCUMENT_WRITE_BLOCKED = 9;
    const {
      Error
    } = globalThis;
    const {
      from
    } = Array;
    const error = Function.prototype.apply.bind(console.error, console);
    function err(code) {
      const args = from(arguments);
      error(args);
      return new Error(code);
    }
    function generateErrorMessage(code) {
      return `SNOW ERROR (CODE:${code}):`;
    }
    function e(msg, a, b, c) {
      switch (msg) {
        case ERR_BLOB_TYPE_BLOCKED:
          const object = a,
            kind = b,
            type = c;
          return err(generateErrorMessage(ERR_BLOB_TYPE_BLOCKED), `blocking ${kind} object:`, object, `of type "${type}" (not in allow list)`, '.', 'if this prevents your application from running correctly, please visit/report at', 'https://github.com/LavaMoat/snow/issues/87#issuecomment-1586868353', '.');
        case ERR_EXTENDING_FRAMABLES_BLOCKED:
          const name = a,
            options = b;
          return err(generateErrorMessage(ERR_EXTENDING_FRAMABLES_BLOCKED), `blocking extension attempt ("${name}") of framable elements such as provided`, options, '.', 'if this prevents your application from running correctly, please visit/report at', 'https://github.com/LavaMoat/snow/issues/56#issuecomment-1374899809', '.');
        case ERR_MARK_NEW_WINDOW_FAILED:
          const win = a,
            exception = b;
          return err(generateErrorMessage(ERR_MARK_NEW_WINDOW_FAILED), 'failed to mark new window:', win, '.', 'if this prevents your application from running correctly, please visit/report at', 'https://github.com/LavaMoat/snow/issues/33#issuecomment-1239280063', '.', 'in order to maintain a bulletproof defense mechanism, failing to mark a new window typically causes an infinite loop', '.', 'error caught:', exception);
        case ERR_CB_MUST_BE_FUNCTION:
          const cb = a;
          return err(generateErrorMessage(ERR_CB_MUST_BE_FUNCTION), 'first argument must be of type "function", instead got:', cb, '.', 'therefore, snow bailed and is not applied to the page until this is fixed.');
        case ERR_OPEN_JS_SCHEME_BLOCKED:
          const url = a,
            win2 = b;
          return err(generateErrorMessage(ERR_OPEN_JS_SCHEME_BLOCKED), 'blocking open attempt to "javascript:" url:', url, 'by window: ', win2, '.', 'if this prevents your application from running correctly, please visit/report at', 'https://github.com/LavaMoat/snow/issues/44#issuecomment-1369687802', '.');
        case ERR_OPENED_PROP_ACCESS_BLOCKED:
          const property = a,
            win3 = b;
          return err(generateErrorMessage(ERR_OPENED_PROP_ACCESS_BLOCKED), 'blocking access to property:', `"${property}"`, 'of opened window: ', win3, '.', 'if this prevents your application from running correctly, please visit/report at', 'https://github.com/LavaMoat/snow/issues/2#issuecomment-1239264255', '.');
        case ERR_DECLARATIVE_SHADOWS_BLOCKED:
          const html = a;
          return err(generateErrorMessage(ERR_DECLARATIVE_SHADOWS_BLOCKED), 'blocking html string that includes a representation of a declarative shadow:', `"${html}"`, '.', 'if this prevents your application from running correctly, please visit/report at', 'https://github.com/LavaMoat/snow/issues/32#issuecomment-1239273328', '.');
        case ERR_HTML_FRAMES_SRCDOC_BLOCKED:
          const html2 = a;
          return err(generateErrorMessage(ERR_HTML_FRAMES_SRCDOC_BLOCKED), 'blocking html string that includes a representation of a framable element with the "srcdoc" attribute:', `"${html2}"`, '.', 'if this prevents your application from running correctly, please visit/report at', 'https://github.com/LavaMoat/snow/issues/???', '.');
        case ERR_NON_TOP_DOCUMENT_WRITE_BLOCKED:
          const document = a;
          return err(generateErrorMessage(ERR_NON_TOP_DOCUMENT_WRITE_BLOCKED), 'blocking document.write\\ln action on a document that is not the top most document:', document, '.', 'if this prevents your application from running correctly, please visit/report at', 'https://github.com/LavaMoat/snow/issues/???', '.');
      }
    }
    module.exports = {
      error: e,
      generateErrorMessage,
      ERR_MARK_NEW_WINDOW_FAILED,
      ERR_OPENED_PROP_ACCESS_BLOCKED,
      ERR_OPEN_JS_SCHEME_BLOCKED,
      ERR_CB_MUST_BE_FUNCTION,
      ERR_DECLARATIVE_SHADOWS_BLOCKED,
      ERR_EXTENDING_FRAMABLES_BLOCKED,
      ERR_BLOB_TYPE_BLOCKED,
      ERR_HTML_FRAMES_SRCDOC_BLOCKED,
      ERR_NON_TOP_DOCUMENT_WRITE_BLOCKED
    };
    
    /***/ }),
    
    /***/ 111:
    /***/ ((module, __unused_webpack_exports, __webpack_require__) => {
    
    const {
      Map,
      Object,
      Array
    } = __webpack_require__(14);
    const secret = new Array();
    const wins = new Map();
    function isMarked(win) {
      if (!wins.has(win)) {
        return false;
      }
      const desc = Object.getOwnPropertyDescriptor(win, 'SNOW_ID');
      if (!desc || !Object.hasOwnProperty.call(desc, 'value')) {
        return false;
      }
      if (typeof desc.value !== 'function') {
        return false;
      }
      const key = wins.get(win);
      const answer = desc.value(secret);
      return answer === key;
    }
    function mark(win) {
      const key = new Array();
      const desc = Object.create(null);
      desc.value = s => s === secret && key;
      Object.defineProperty(win, 'SNOW_ID', desc);
      wins.set(win, key);
    }
    module.exports = {
      isMarked,
      mark
    };
    
    /***/ }),
    
    /***/ 14:
    /***/ ((module, __unused_webpack_exports, __webpack_require__) => {
    
    const {
      runInNewRealm
    } = __webpack_require__(407);
    function natives(win) {
      const {
        EventTarget
      } = win; // PR#62
      return runInNewRealm(function (win) {
        const {
          URL,
          Proxy,
          JSON,
          Attr,
          String,
          Function,
          Map,
          Node,
          Document,
          DocumentFragment,
          Blob,
          ShadowRoot,
          Object,
          Reflect,
          Array,
          Element,
          HTMLElement,
          Range,
          HTMLIFrameElement,
          HTMLFrameElement,
          HTMLObjectElement
        } = win;
        const bag = {
          URL,
          Proxy,
          JSON,
          Attr,
          String,
          Function,
          Map,
          Node,
          Document,
          DocumentFragment,
          Blob,
          ShadowRoot,
          Object,
          Reflect,
          Array,
          Element,
          HTMLElement,
          Range,
          EventTarget,
          HTMLIFrameElement,
          HTMLFrameElement,
          HTMLObjectElement
        };
        bag.document = {
          createElement: win.document.createElement.bind(win.document)
        };
        return bag;
      });
    }
    function setup(win) {
      const bag = natives(win);
      const {
        document,
        Proxy,
        Function,
        String,
        Map,
        Node,
        Document,
        DocumentFragment,
        Blob,
        ShadowRoot,
        Object,
        Reflect,
        Array,
        Element,
        HTMLElement,
        Range,
        EventTarget,
        HTMLIFrameElement,
        HTMLFrameElement,
        HTMLObjectElement
      } = bag;
      Object.assign(bag, {
        iframeContentWindow: Object.getOwnPropertyDescriptor(HTMLIFrameElement.prototype, 'contentWindow').get,
        frameContentWindow: Object.getOwnPropertyDescriptor(HTMLFrameElement.prototype, 'contentWindow').get,
        objectContentWindow: Object.getOwnPropertyDescriptor(HTMLObjectElement.prototype, 'contentWindow').get,
        createElement: Object.getOwnPropertyDescriptor(Document.prototype, 'createElement').value,
        slice: Object.getOwnPropertyDescriptor(Array.prototype, 'slice').value,
        push: Object.getOwnPropertyDescriptor(Array.prototype, 'push').value,
        split: Object.getOwnPropertyDescriptor(String.prototype, 'split').value,
        nodeType: Object.getOwnPropertyDescriptor(Node.prototype, 'nodeType').get,
        tagName: Object.getOwnPropertyDescriptor(Element.prototype, 'tagName').get,
        getInnerHTML: Object.getOwnPropertyDescriptor(Element.prototype, 'innerHTML').get,
        setInnerHTML: Object.getOwnPropertyDescriptor(Element.prototype, 'innerHTML').set,
        toString: Object.getOwnPropertyDescriptor(Object.prototype, 'toString').value,
        getOnload: Object.getOwnPropertyDescriptor(HTMLElement.prototype, 'onload').get,
        setOnload: Object.getOwnPropertyDescriptor(HTMLElement.prototype, 'onload').set,
        getAttribute: Object.getOwnPropertyDescriptor(Element.prototype, 'getAttribute').value,
        setAttribute: Object.getOwnPropertyDescriptor(Element.prototype, 'setAttribute').value,
        removeAttribute: Object.getOwnPropertyDescriptor(Element.prototype, 'removeAttribute').value,
        remove: Object.getOwnPropertyDescriptor(Element.prototype, 'remove').value,
        addEventListener: Object.getOwnPropertyDescriptor(EventTarget.prototype, 'addEventListener').value,
        removeEventListener: Object.getOwnPropertyDescriptor(EventTarget.prototype, 'removeEventListener').value,
        getChildElementCount: Object.getOwnPropertyDescriptor(Element.prototype, 'childElementCount').get,
        getFrameElement: Object.getOwnPropertyDescriptor(win, 'frameElement').get,
        getParentElement: Object.getOwnPropertyDescriptor(Node.prototype, 'parentElement').get,
        getOwnerDocument: Object.getOwnPropertyDescriptor(Node.prototype, 'ownerDocument').get,
        getDefaultView: Object.getOwnPropertyDescriptor(Document.prototype, 'defaultView').get,
        getBlobFileType: Object.getOwnPropertyDescriptor(Blob.prototype, 'type').get,
        getPreviousElementSibling: Object.getOwnPropertyDescriptor(Element.prototype, 'previousElementSibling').get,
        getCommonAncestorContainer: Object.getOwnPropertyDescriptor(Range.prototype, 'commonAncestorContainer').get
      });
      return {
        document,
        Proxy,
        Object,
        Reflect,
        Function,
        Node,
        Element,
        Document,
        DocumentFragment,
        Blob,
        ShadowRoot,
        Array,
        Map,
        getContentWindow,
        stringToLowerCase,
        stringStartsWith,
        parse,
        stringify,
        slice,
        push,
        split,
        nodeType,
        tagName,
        toString,
        getOnload,
        setOnload,
        remove,
        removeAttribute,
        getAttribute,
        setAttribute,
        addEventListener,
        removeEventListener,
        createElement,
        getInnerHTML,
        setInnerHTML,
        getChildElementCount,
        getFrameElement,
        getParentElement,
        getOwnerDocument,
        getDefaultView,
        getBlobFileType,
        getPreviousElementSibling,
        getCommonAncestorContainer
      };
      function getContentWindow(element, tag) {
        switch (tag) {
          case 'IFRAME':
            return bag.iframeContentWindow.call(element);
          case 'FRAME':
            return bag.frameContentWindow.call(element);
          case 'OBJECT':
            return bag.objectContentWindow.call(element);
          case 'EMBED':
            return null;
          default:
            return null;
        }
      }
      function stringToLowerCase(string) {
        return bag.String.prototype.toLowerCase.call(string);
      }
      function stringStartsWith(string, find) {
        return bag.String.prototype.startsWith.call(string, find);
      }
      function parse(text, reviver) {
        return bag.JSON.parse(text, reviver);
      }
      function stringify(value, replacer, space) {
        return bag.JSON.stringify(value, replacer, space);
      }
      function slice(arr, start, end) {
        return bag.slice.call(arr, start, end);
      }
      function push(arr, item) {
        return bag.push.call(arr, item);
      }
      function split(string, delimiter) {
        return bag.split.call(string, delimiter);
      }
      function nodeType(node) {
        return bag.nodeType.call(node);
      }
      function tagName(element) {
        return bag.tagName.call(element);
      }
      function toString(object) {
        return bag.toString.call(object);
      }
      function getOnload(element) {
        return bag.getOnload.call(element);
      }
      function setOnload(element, onload) {
        return bag.setOnload.call(element, onload);
      }
      function remove(element) {
        return bag.remove.call(element);
      }
      function removeAttribute(element, attribute) {
        return bag.removeAttribute.call(element, attribute);
      }
      function getAttribute(element, attribute) {
        return bag.getAttribute.call(element, attribute);
      }
      function setAttribute(element, attribute, value) {
        return bag.setAttribute.call(element, attribute, value);
      }
      function addEventListener(element, event, listener, options) {
        return bag.Function.prototype.call.call(bag.addEventListener, element, event, listener, options);
      }
      function removeEventListener(element, event, listener, options) {
        return bag.Function.prototype.call.call(bag.removeEventListener, element, event, listener, options);
      }
      function createElement(document, tagName, options) {
        return bag.createElement.call(document, tagName, options);
      }
      function getInnerHTML(element) {
        return bag.getInnerHTML.call(element);
      }
      function setInnerHTML(element, html) {
        return bag.setInnerHTML.call(element, html);
      }
      function getChildElementCount(element) {
        return bag.getChildElementCount.call(element);
      }
      function getFrameElement(win) {
        return bag.Function.prototype.call.call(bag.getFrameElement, win);
      }
      function getParentElement(element) {
        return bag.getParentElement.call(element);
      }
      function getOwnerDocument(node) {
        return bag.getOwnerDocument.call(node);
      }
      function getDefaultView(document) {
        return bag.getDefaultView.call(document);
      }
      function getBlobFileType(blob) {
        return bag.getBlobFileType.call(blob);
      }
      function getPreviousElementSibling(node) {
        return bag.getPreviousElementSibling.call(node);
      }
      function getCommonAncestorContainer(range) {
        return bag.getCommonAncestorContainer.call(range);
      }
    }
    module.exports = setup(top);
    
    /***/ }),
    
    /***/ 583:
    /***/ ((module, __unused_webpack_exports, __webpack_require__) => {
    
    const {
      stringToLowerCase,
      stringStartsWith,
      slice,
      Function,
      Object
    } = __webpack_require__(14);
    const {
      error,
      ERR_OPEN_JS_SCHEME_BLOCKED
    } = __webpack_require__(312);
    const {
      proxy,
      getProxyByOpened
    } = __webpack_require__(134);
    function hookMessageEvent(win) {
      const desc = Object.getOwnPropertyDescriptor(win.MessageEvent.prototype, 'source');
      const get = desc.get;
      desc.get = function () {
        const source = get.call(this);
        return getProxyByOpened(source) || source;
      };
      Object.defineProperty(win.MessageEvent.prototype, 'source', desc);
    }
    function hook(win, native, cb, isWindowProxy) {
      cb(win);
      return function open() {
        const args = slice(arguments);
        const url = args[0];
        if (stringStartsWith(stringToLowerCase(url + ''), 'javascript')) {
          throw error(ERR_OPEN_JS_SCHEME_BLOCKED, url + '', win);
        }
        const opened = Function.prototype.apply.call(native, this, args);
        if (!opened) {
          return null;
        }
        if (!isWindowProxy && args.length < 3) {
          return opened;
        }
        return proxy(opened);
      };
    }
    function hookOpen(win) {
      Object.defineProperty(win, 'open', {
        value: hook(win, win.open, hookMessageEvent, true)
      });
      Object.defineProperty(win.Document.prototype, 'open', {
        value: hook(win, win.document.open, hookMessageEvent, false)
      });
    }
    module.exports = hookOpen;
    
    /***/ }),
    
    /***/ 134:
    /***/ ((module, __unused_webpack_exports, __webpack_require__) => {
    
    const {
      Object,
      Proxy,
      Reflect,
      Map
    } = __webpack_require__(14);
    const {
      error,
      ERR_OPENED_PROP_ACCESS_BLOCKED
    } = __webpack_require__(312);
    const openeds = new Map();
    function getProxyByOpened(opened) {
      return openeds.get(opened);
    }
    function forEachOpened(cb, arg1) {
      for (const opened of openeds.keys()) {
        cb(opened, arg1);
      }
    }
    function proxy(opened) {
      const target = Object.create(null);
      Object.defineProperty(target, 'closed', {
        get: function () {
          return opened.closed;
        }
      });
      Object.defineProperty(target, 'close', {
        value: function () {
          return opened.close();
        }
      });
      Object.defineProperty(target, 'focus', {
        value: function () {
          return opened.focus();
        }
      });
      Object.defineProperty(target, 'postMessage', {
        value: function (message, targetOrigin, transfer) {
          return opened.postMessage(message, targetOrigin, transfer);
        }
      });
      if (!openeds.has(opened)) {
        top['SNOW_WINDOW'](opened);
        const p = new Proxy(target, {
          get: function (target, property) {
            let ret = Reflect.get(target, property);
            if (Reflect.has(target, property)) {
              return ret;
            }
            if (Reflect.has(opened, property)) {
              throw error(ERR_OPENED_PROP_ACCESS_BLOCKED, property, opened);
            }
            return ret;
          },
          set: function () {}
        });
        openeds.set(opened, p);
      }
      return getProxyByOpened(opened);
    }
    module.exports = {
      proxy,
      getProxyByOpened,
      forEachOpened
    };
    
    /***/ }),
    
    /***/ 278:
    /***/ ((module, __unused_webpack_exports, __webpack_require__) => {
    
    const {
      Object,
      slice,
      Function
    } = __webpack_require__(14);
    const {
      proxy
    } = __webpack_require__(134);
    function hookDocumentPictureInPicture(win, prop) {
      const desc = Object.getOwnPropertyDescriptor(win[prop].prototype, 'window');
      const get = desc.get;
      desc.get = function () {
        return proxy(get.call(this));
      };
      Object.defineProperty(win[prop].prototype, 'window', desc);
    }
    function hook(win, native, cb) {
      cb(win, 'DocumentPictureInPictureEvent');
      cb(win, 'DocumentPictureInPicture');
      return async function open() {
        const args = slice(arguments);
        const opened = await Function.prototype.apply.call(native, this, args);
        if (!opened) {
          return null;
        }
        return proxy(opened);
      };
    }
    function hookRequest(win) {
      if (!win?.documentPictureInPicture?.requestWindow) {
        return;
      }
      win.documentPictureInPicture.requestWindow = hook(win, win.documentPictureInPicture.requestWindow, hookDocumentPictureInPicture);
    }
    module.exports = hookRequest;
    
    /***/ }),
    
    /***/ 373:
    /***/ ((module, __unused_webpack_exports, __webpack_require__) => {
    
    const hook = __webpack_require__(228);
    const {
      getFramesArray,
      shadows
    } = __webpack_require__(648);
    const {
      Object,
      Function
    } = __webpack_require__(14);
    function protectShadows(connectedOnly) {
      for (let i = 0; i < shadows.length; i++) {
        const shadow = shadows[i];
        if (connectedOnly && !shadow.isConnected) {
          continue;
        }
        const frames = getFramesArray(shadow, false);
        hook(frames);
      }
    }
    function getHook(win, native) {
      return function (options) {
        const ret = Function.prototype.call.call(native, this, options);
        shadows.push(ret);
        protectShadows(true);
        return ret;
      };
    }
    function hookShadowDOM(win) {
      const desc = Object.getOwnPropertyDescriptor(win.Element.prototype, 'attachShadow');
      desc.configurable = desc.writable = true;
      const val = desc.value;
      desc.value = getHook(win, val);
      Object.defineProperty(win.Element.prototype, 'attachShadow', desc);
    }
    module.exports = {
      hookShadowDOM,
      protectShadows
    };
    
    /***/ }),
    
    /***/ 294:
    /***/ ((module, __unused_webpack_exports, __webpack_require__) => {
    
    const {
      trustedHTMLs
    } = __webpack_require__(648);
    const {
      Object,
      Function
    } = __webpack_require__(14);
    function getHook(win, native) {
      trustedHTMLs.push(win.trustedTypes.emptyHTML);
      return function (a, b) {
        const ret = Function.prototype.call.call(native, this, a, b);
        trustedHTMLs.push(ret);
        return ret;
      };
    }
    function hookTrustedHTMLs(win) {
      if (typeof win.TrustedTypePolicy === 'undefined') {
        return;
      }
      const desc = Object.getOwnPropertyDescriptor(win.TrustedTypePolicy.prototype, 'createHTML');
      desc.configurable = desc.writable = true;
      const val = desc.value;
      desc.value = getHook(win, val);
      Object.defineProperty(win.TrustedTypePolicy.prototype, 'createHTML', desc);
    }
    module.exports = hookTrustedHTMLs;
    
    /***/ }),
    
    /***/ 716:
    /***/ ((module, __unused_webpack_exports, __webpack_require__) => {
    
    const {
      Object,
      Array,
      getBlobFileType
    } = __webpack_require__(14);
    const {
      error,
      ERR_BLOB_TYPE_BLOCKED
    } = __webpack_require__(312);
    const KIND = 'KIND',
      TYPE = 'TYPE';
    const BLOB = 'Blob',
      FILE = 'File',
      MEDIA_SOURCE = 'MediaSource';
    
    // blobs that were JS crafted by Blob constructor rather than naturally created by the browser from a remote resource
    const artificialBlobs = new Array();
    const allowedTypes = new Array('', 'text/javascript', 'text/css', 'application/javascript', 'application/css', 'image/jpeg', 'image/jpg', 'image/png', 'audio/ogg; codecs=opus', 'video/mp4', 'application/pdf', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
    function getHook(native, kind) {
      return function (a, b) {
        const ret = new native(a, b);
        Object.defineProperty(ret, KIND, {
          value: kind
        });
        if (kind === BLOB || kind === FILE) {
          Object.defineProperty(ret, TYPE, {
            value: getBlobFileType(ret)
          });
        }
        artificialBlobs.push(ret);
        return ret;
      };
    }
    function hookBlob(win) {
      const native = win[BLOB];
      const hook = getHook(native, BLOB);
      function Blob(a, b) {
        return hook(a, b);
      }
      // to pass 'Blob.prototype.isPrototypeOf(b)' test (https://github.com/LavaMoat/snow/issues/87#issue-1751534810)
      Object.setPrototypeOf(native.prototype, Blob.prototype);
      win[BLOB] = Blob;
      Object.defineProperty(native.prototype, 'constructor', {
        value: Blob
      });
    }
    function hookFile(win) {
      const native = win[FILE];
      const hook = getHook(native, FILE);
      function File(a, b) {
        return hook(a, b);
      }
      // to pass 'File.prototype.isPrototypeOf(f)' test (https://github.com/LavaMoat/snow/issues/87#issue-1751534810)
      Object.setPrototypeOf(native.prototype, File.prototype);
      win[FILE] = File;
      Object.defineProperty(native.prototype, 'constructor', {
        value: File
      });
    }
    function hookMediaSource(win) {
      const native = win[MEDIA_SOURCE];
      const hook = getHook(native, MEDIA_SOURCE);
      function MediaSource(a, b) {
        return hook(a, b);
      }
      // MediaSource is expected to have static own props (e.g. isTypeSupported)
      Object.setPrototypeOf(MediaSource, native);
      win[MEDIA_SOURCE] = MediaSource;
      Object.defineProperty(native.prototype, 'constructor', {
        value: MediaSource
      });
    }
    function isBlobArtificial(object) {
      return artificialBlobs.includes(object);
    }
    function assertTypeIsForbidden(object) {
      const kind = object[KIND];
      if (kind === BLOB || kind === FILE) {
        const type = object[TYPE];
        if (!allowedTypes.includes(type)) {
          throw error(ERR_BLOB_TYPE_BLOCKED, object, kind, type);
        }
      }
    }
    function hook(win) {
      const native = win.URL.createObjectURL;
      function createObjectURL(object) {
        if (isBlobArtificial(object)) {
          assertTypeIsForbidden(object);
        }
        return native(object);
      }
      Object.defineProperty(win.URL, 'createObjectURL', {
        value: createObjectURL
      });
    }
    function hookCreateObjectURL(win) {
      hook(win);
      hookBlob(win);
      hookFile(win);
      hookMediaSource(win);
    }
    module.exports = hookCreateObjectURL;
    
    /***/ }),
    
    /***/ 648:
    /***/ ((module, __unused_webpack_exports, __webpack_require__) => {
    
    const {
      tagName,
      nodeType,
      slice,
      Array,
      parse,
      stringify,
      Node,
      Document,
      DocumentFragment,
      Element,
      ShadowRoot,
      getContentWindow,
      getDefaultView,
      getOwnerDocument,
      stringToLowerCase,
      Object
    } = __webpack_require__(14);
    const shadows = new Array(),
      trustedHTMLs = new Array();
    function isShadow(node) {
      return shadows.includes(node);
    }
    function isTrustedHTML(node) {
      return trustedHTMLs.includes(node);
    }
    function makeDescriptorSetter(prop, val) {
      const desc = Object.create(null);
      desc.value = val;
      return function (obj) {
        if (!Object.getOwnPropertyDescriptor(obj, prop)) {
          Object.defineProperty(obj, prop, desc);
        }
      };
    }
    function getPrototype(node) {
      if (isShadow(node)) {
        return ShadowRoot;
      }
      switch (nodeType(node)) {
        case Node.prototype.DOCUMENT_NODE:
          return Document;
        case Node.prototype.DOCUMENT_FRAGMENT_NODE:
          return DocumentFragment;
        default:
          return Element;
      }
    }
    function isTagFramable(t) {
      const tag = stringToLowerCase(t);
      return tag === 'iframe' || tag === 'frame' || tag === 'object' || tag === 'embed';
    }
    function getFrameTag(element) {
      if (!element || typeof element !== 'object') {
        return null;
      }
      if (nodeType(element) !== Element.prototype.ELEMENT_NODE) {
        return null;
      }
      if (isShadow(element)) {
        return null;
      }
      const tag = tagName(element);
      if (!isTagFramable(tag)) {
        return null;
      }
      return tag;
    }
    function toArray(item) {
      if (!Array.isArray(item)) {
        item = new Array(item);
      }
      return item;
    }
    function getContentWindowOfFrame(iframe) {
      return getContentWindow(iframe, getFrameTag(iframe));
    }
    function getOwnerWindowOfNode(iframe) {
      return getDefaultView(getOwnerDocument(iframe));
    }
    function canNodeRunQuerySelector(node) {
      if (isShadow(node)) {
        return true;
      }
      const type = nodeType(node);
      return type === Element.prototype.ELEMENT_NODE || type === Element.prototype.DOCUMENT_FRAGMENT_NODE || type === Element.prototype.DOCUMENT_NODE;
    }
    function getDeclarativeShadows(element) {
      const querySelectorAll = getPrototype(element).prototype.querySelectorAll;
      return querySelectorAll.call(element, 'template[shadowroot]');
    }
    function getFramesArray(element, includingParent) {
      const frames = new Array();
      if (null === element || typeof element !== 'object') {
        return frames;
      }
      if (isTrustedHTML(element) || !canNodeRunQuerySelector(element)) {
        return frames;
      }
      const querySelectorAll = getPrototype(element).prototype.querySelectorAll;
      const list = querySelectorAll.call(element, 'iframe,frame,object,embed');
      fillArrayUniques(frames, slice(list));
      if (includingParent) {
        fillArrayUniques(frames, toArray(element));
      }
      return frames;
    }
    function fillArrayUniques(arr, items) {
      let isArrUpdated = false;
      for (let i = 0; i < items.length; i++) {
        if (!arr.includes(items[i])) {
          arr.push(items[i]);
          isArrUpdated = true;
        }
      }
      return isArrUpdated;
    }
    module.exports = {
      getDeclarativeShadows,
      makeDescriptorSetter,
      toArray,
      isTagFramable,
      getOwnerWindowOfNode,
      getContentWindowOfFrame,
      getFramesArray,
      getFrameTag,
      shadows,
      trustedHTMLs
    };
    
    /***/ }),
    
    /***/ 744:
    /***/ ((module, __unused_webpack_exports, __webpack_require__) => {
    
    const {
      runInNewRealm
    } = __webpack_require__(407);
    const {
      Map,
      toString,
      stringStartsWith,
      Blob
    } = __webpack_require__(14);
    const blobs = new Map();
    const {
      createObjectURL,
      revokeObjectURL
    } = URL;
    const BLOCKED_BLOB_MSG = `
    BLOCKED BY SNOW:
    Creating URL objects is not allowed under Snow protection within Web Workers.
    If this prevents your application from running correctly, please visit/report at https://github.com/LavaMoat/snow/pull/89#issuecomment-1589359673.
    Learn more at https://github.com/LavaMoat/snow/pull/89`;
    function syncGet(url) {
      return runInNewRealm(function (win) {
        let content;
        const xhr = new win.XMLHttpRequest();
        xhr.open('GET', url, false);
        xhr.onreadystatechange = function () {
          if (xhr.readyState === 4 && xhr.status === 200) {
            content = xhr.responseText;
          }
        };
        xhr.send();
        return content;
      });
    }
    function swap(url) {
      if (!blobs.has(url)) {
        const content = syncGet(url);
        const prefix = `(function() { Object.defineProperty(URL, 'createObjectURL', { value: () => { throw new Error(\`${BLOCKED_BLOB_MSG}\`) }}) }())`;
        const js = prefix + '\n\n' + content;
        blobs.set(url, createObjectURL(new Blob([js], {
          type: 'text/javascript'
        })));
      }
      return blobs.get(url);
    }
    function hookRevokeObjectURL(win) {
      win.URL.revokeObjectURL = function (objectURL) {
        const url = blobs.get(objectURL);
        if (url) {
          revokeObjectURL(url);
          blobs.delete(url);
        }
        return revokeObjectURL(objectURL);
      };
    }
    function hook(win) {
      const native = win.Worker;
      win.Worker = function Worker(aURL, options) {
        const url = typeof aURL === 'string' ? aURL : toString(aURL);
        if (stringStartsWith(url, 'blob')) {
          return new native(swap(url), options);
        }
        return new native(url, options);
      };
    }
    function hookWorker(win) {
      hookRevokeObjectURL(win);
      hook(win);
    }
    module.exports = hookWorker;
    
    /***/ })
    
    /******/ 	});
    /************************************************************************/
    /******/ 	// The module cache
    /******/ 	var __webpack_module_cache__ = {};
    /******/ 	
    /******/ 	// The require function
    /******/ 	function __webpack_require__(moduleId) {
    /******/ 		// Check if module is in cache
    /******/ 		var cachedModule = __webpack_module_cache__[moduleId];
    /******/ 		if (cachedModule !== undefined) {
    /******/ 			return cachedModule.exports;
    /******/ 		}
    /******/ 		// Create a new module (and put it into the cache)
    /******/ 		var module = __webpack_module_cache__[moduleId] = {
    /******/ 			// no module.id needed
    /******/ 			// no module.loaded needed
    /******/ 			exports: {}
    /******/ 		};
    /******/ 	
    /******/ 		// Execute the module function
    /******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
    /******/ 	
    /******/ 		// Return the exports of the module
    /******/ 		return module.exports;
    /******/ 	}
    /******/ 	
    /************************************************************************/
    /******/ 	/* webpack/runtime/compat get default export */
    /******/ 	(() => {
    /******/ 		// getDefaultExport function for compatibility with non-harmony modules
    /******/ 		__webpack_require__.n = (module) => {
    /******/ 			var getter = module && module.__esModule ?
    /******/ 				() => (module['default']) :
    /******/ 				() => (module);
    /******/ 			__webpack_require__.d(getter, { a: getter });
    /******/ 			return getter;
    /******/ 		};
    /******/ 	})();
    /******/ 	
    /******/ 	/* webpack/runtime/define property getters */
    /******/ 	(() => {
    /******/ 		// define getter functions for harmony exports
    /******/ 		__webpack_require__.d = (exports, definition) => {
    /******/ 			for(var key in definition) {
    /******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
    /******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
    /******/ 				}
    /******/ 			}
    /******/ 		};
    /******/ 	})();
    /******/ 	
    /******/ 	/* webpack/runtime/hasOwnProperty shorthand */
    /******/ 	(() => {
    /******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
    /******/ 	})();
    /******/ 	
    /************************************************************************/
    var __webpack_exports__ = {};
    // This entry need to be wrapped in an IIFE because it need to be in strict mode.
    (() => {
    "use strict";
    /* harmony import */ var _src_index__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(352);
    /* harmony import */ var _src_index__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_src_index__WEBPACK_IMPORTED_MODULE_0__);
    
    (function (win) {
      Object.defineProperty(win, 'SNOW', {
        value: function (cb, w) {
          func(cb, w || win);
        }
      });
      let func = (_src_index__WEBPACK_IMPORTED_MODULE_0___default());
      if (win !== top) {
        func = top.SNOW;
        win.SNOW(() => {}, win);
      }
    })(window);
    })();
    
    /******/ })()
    ;
    }())