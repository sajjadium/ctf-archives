import sanitizeHTML from '../security/sanitizeHTML';

export default function parseMarkdown(markdown: string) {
    const parser = require('markdown-it')().use(require('markdown-it-attrs'), {
        allowedAttributes: [ 'id', 'class', 'name' ]
    }).disable('emphasis');
    var unsafe_html = parser.render(markdown);

    return sanitizeHTML(unsafe_html);
}