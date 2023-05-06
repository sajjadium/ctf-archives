const createDOMPurify = require('dompurify');
const { JSDOM } = require('jsdom');

const window = new JSDOM('').window;
const DOMPurify = createDOMPurify(window);

function my_sanitize(html) {
    const document = new JSDOM('').window.document
    document.body.outerHTML = html

    let node;
    const iter = document.createNodeIterator(document.body)

    while (node = iter.nextNode()) {
        if (/(script|iframe|frame|object|data|m.+)/i.test(node.nodeName)) {
            node.parentNode.removeChild(node)
            continue
        }


        if (node.attributes) {
            for (let i = node.attributes.length - 1; i >= 0; i--) {
                const att = node.attributes[i]
                if (! /(class|src|style)/i.test(att.name)) {
                    node.removeAttributeNode(att)
                }
            }
        }
    }

    return document.body.innerHTML
}

function sanitize(html) {

    let clean = my_sanitize(html)

    clean = DOMPurify.sanitize(clean)

    return clean
}


module.exports = { sanitize }