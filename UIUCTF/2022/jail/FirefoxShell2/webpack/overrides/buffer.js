/*!
 * The buffer module from node.js, for the browser.
 *
 * @author   Feross Aboukhadijeh <https://feross.org>
 * @license  MIT
 */
// Source: https://github.com/feross/buffer/blob/master/index.js

'use strict';

module.exports = {
  Buffer: {
    prototype: {
      hexSlice(start, end) {
        const len = this.length;

        if (!start || start < 0) {
          start = 0;
        }
        if (!end || end < 0 || end > len) {
          end = len;
        }

        let out = '';
        for (let i = start; i < end; ++i) {
          out += hexSliceLookupTable[this[i]];
        }

        return out;
      },
    },
  },
};

const hexSliceLookupTable = (function() {
  const alphabet = '0123456789abcdef';
  const table = new Array(256);
  for (let i = 0; i < 16; ++i) {
    const i16 = i * 16;
    for (let j = 0; j < 16; ++j) {
      table[i16 + j] = alphabet[i] + alphabet[j];
    }
  }
  return table;
})();
