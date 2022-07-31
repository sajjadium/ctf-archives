/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */
'use strict';

const EXPORTED_SYMBOLS = ['Stdout'];

/* global OS */
const { ctypes } = ChromeUtils.import('resource://gre/modules/ctypes.jsm');
Cc['@mozilla.org/net/osfileconstantsservice;1'].getService(Ci.nsIOSFileConstantsService).init();

const libc = ctypes.open('libc.so.6');
const LIBC = OS.Constants.libc;
const write = libc.declare(
  'write',
  ctypes.default_abi,
  ctypes.ssize_t,
  ctypes.int,
  ctypes.char.ptr,
  ctypes.size_t
);

const Stdout = {
  writeBuffer(buffer) {
    while (buffer.byteLength) {
      const size = write(1, buffer, buffer.byteLength);
      if (size < 0 && ctypes.errno === LIBC.EAGAIN) {
        continue;
      }

      if (size <= 0) {
        throw new Error(`Error writing stdout, errno = ${ctypes.errno}`);
      }

      if (size === buffer.byteLength) {
        return;
      }

      buffer = buffer.slice(size);
    }
  },

  write(string) {
    return this.writeBuffer(new TextEncoder().encode(string).buffer);
  },
};
