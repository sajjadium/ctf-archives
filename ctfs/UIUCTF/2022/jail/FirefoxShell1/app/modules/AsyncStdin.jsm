/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */
'use strict';

const EXPORTED_SYMBOLS = ['AsyncStdin', 'AsyncStdinWorker'];

const { ctypes } = ChromeUtils.import('resource://gre/modules/ctypes.jsm');
const libc = ctypes.open('libc.so.6');
const eventfd_write = libc.declare(
  'eventfd_write',
  ctypes.default_abi,
  ctypes.int,
  ctypes.int,
  ctypes.uint64_t
);

const pending_promises = [];
const pending_data = [];
let efd = undefined;
let EOF = false;

const doPromised = function() {
  if (!pending_promises.length) {
    return;
  }

  const [endcond, resolve] = pending_promises[0];
  let ret = new ArrayBuffer(0);

  const append = function(buffer) {
    const tmp = new Uint8Array(ret.byteLength + buffer.byteLength);
    tmp.set(new Uint8Array(ret), 0);
    tmp.set(new Uint8Array(buffer), ret.byteLength);
    return tmp.buffer;
  };

  while (true) {
    const [end, sliceat] = endcond(ret);

    if (end) {
      if (sliceat < ret.byteLength) {
        pending_data.unshift(ret.slice(sliceat));
        ret = ret.slice(0, sliceat);
      }

      break;
    } else if (pending_data.length) {
      ret = append(pending_data.shift());
    } else if (EOF) {
      break;
    } else {
      if (ret.byteLength) {
        pending_data.unshift(ret);
      }
      return;
    }
  }

  pending_promises.shift();

  resolve(ret);
};

const AsyncStdinWorker = new ChromeWorker('resource:///modules/AsyncStdinWorker.js');
AsyncStdinWorker.addEventListener('message', function(msg) {
  if (efd === undefined) {
    if (msg.data < 0) {
      throw new Error('AsyncStdinWorker eventfd fail');
    } else {
      efd = msg.data;
    }
  } else {
    if (msg.data === null) {
      EOF = true;
    } else {
      pending_data.push(msg.data);
    }

    doPromised();
  }
});

const AsyncStdin = {
  readBuffer(size) {
    return new Promise((resolve, reject) => {
      const endcond = function(buffer) {
        return [buffer.byteLength >= size, size];
      };

      pending_promises.push([endcond, resolve, reject]);
      doPromised();
    });
  },

  async readString(size) {
    const enc = new TextDecoder('utf-8');
    return enc.decode(new Uint8Array(await this.readString(size)));
  },

  async readLine() {
    const enc = new TextDecoder('utf-8');
    const buffer = await new Promise((resolve, reject) => {
      const endcond = function(buffer) {
        const ind = new Uint8Array(buffer).indexOf('\n'.charCodeAt(0));
        return [ind >= 0, ind + 1];
      };

      pending_promises.push([endcond, resolve, reject]);
      doPromised();
    });

    return enc.decode(new Uint8Array(buffer));
  },

  terminate() {
    if (!EOF && efd !== undefined) {
      eventfd_write(efd, 1);
    }

    EOF = true;
  },
};
