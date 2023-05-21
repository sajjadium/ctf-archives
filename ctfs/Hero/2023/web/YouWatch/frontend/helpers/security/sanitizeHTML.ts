import santize from 'sanitize-html';

export default function sanitizeHTML(html) {
    return santize(html, {
        allowedTags: ['h1', 'h2', 'h3', 'h4', 'p', 'div', 'img', 'em', 'a', 'i', 'b'],
        allowedAttributes: {
            '*': [ 'id', 'class', 'name' ],
            'img': [ 'src' ],
            'a': [ 'href' ]
        }
    })
}