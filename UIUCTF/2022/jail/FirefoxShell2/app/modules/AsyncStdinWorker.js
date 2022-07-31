/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */
'use strict';

/* eslint-env mozilla/chrome-worker */
/* global OS */

// ctypes & OS are made available by ChromeWorker, but console.log is
// unavailable. To debug by printing, use dump()

const libc = ctypes.open('libc.so.6');
const LIBC = OS.Constants.libc;
const read = libc.declare(
  'read',
  ctypes.default_abi,
  ctypes.ssize_t,
  ctypes.int,
  ctypes.char.ptr,
  ctypes.size_t
);

const eventfd = libc.declare(
  'eventfd',
  ctypes.default_abi,
  ctypes.int,
  ctypes.unsigned_int,
  ctypes.int
);

const pollfd = ctypes.StructType('pollfd', [
  { fd: ctypes.int },
  { events: ctypes.short },
  { revents: ctypes.short },
]);
const pollfd_arr = ctypes.ArrayType(pollfd);
const poll = libc.declare(
  'poll',
  ctypes.default_abi,
  ctypes.int,
  pollfd_arr,
  ctypes.unsigned_long,
  ctypes.int
);

const POLLIN = 0x0001;
// const POLLPRI = 0x0002
// const POLLOUT = 0x0004
// const POLLERR = 0x0008
// const POLLHUP = 0x0010
// const POLLNVAL = 0x0020

(function() {
  const efd = eventfd(0, LIBC.O_CLOEXEC);
  self.postMessage(efd);

  if (efd < 0) {
    return;
  }

  const fds = pollfd_arr(2);
  fds[0].fd = 0;
  fds[0].events = POLLIN;
  fds[1].fd = efd;
  fds[1].events = POLLIN;

  while (true) {
    poll(fds, 2, -1);

    if (fds[0].revents) {
      const buffer = new ArrayBuffer(2);

      const size = read(0, buffer, buffer.byteLength);
      if (size < 0 && ctypes.errno === LIBC.EAGAIN) {
        continue;
      }

      if (size <= 0) {
        self.postMessage(null);
        break;
      }

      if (size < buffer.byteLength) {
        self.postMessage(buffer.slice(0, size));
        continue;
      }

      self.postMessage(buffer);
    }

    if (fds[1].revents) {
      break;
    }
  }
})();
