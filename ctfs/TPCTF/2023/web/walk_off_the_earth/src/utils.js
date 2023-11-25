const exp = require('constants');
const crypto = require('crypto');
const { JSDOM } = require('jsdom');

const window = new JSDOM('').window;

const dict = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#';

const randomString = (length) => {
    let result = '';
    for (let i = 0; i < length; i++) {
        result += dict[Math.floor(Math.random() * dict.length)];
    }
    return result;
}


function custom_sanitize(html) {
    const BLOCKED_TAG = /(script|iframe|a|img|svg|audio|video)$/i
    const BLOCKED_ATTR = /(href|src|on.+)/i

    const document = new JSDOM('').window.document
    document.body.innerHTML = html
    let node;
    const iter = document.createNodeIterator(document.body)
    while (node = iter.nextNode()) {
        if (node.tagName) {
            if (BLOCKED_TAG.test(node.tagName)) {
                node.remove()
                continue
            }
        }

        if (node.attributes) {
            for (let i = node.attributes.length - 1; i >= 0; i--) {
                const att = node.attributes[i]
                if (BLOCKED_ATTR.test(att.name)) {
                    node.removeAttributeNode(att)
                }
            }
        }
    }

    return document.body.innerHTML
}

const sanitize = (html) => {

    let clean = custom_sanitize(html)

    return clean
}

exports.sanitize = sanitize;
exports.generatePow = generatePow;
exports.checkPow = checkPow;

