class HtmlPurify {
  constructor() {
    this.ALLOWED_HTML = [
      '#text',
      'a',
      'h1',
      'h2',
      'h3',
      'div',
      'img',
      'p',
      'b',
      'template',
      'noscript',
      'textarea',
      'html',
      'head',
      'body'
    ]
  }

  sanitize(html) {
    var dp = new DOMParser();
    var dom = dp.parseFromString(html,'text/html');
    this.cleanNodes(dom.documentElement.childNodes,dom.documentElement)
    return dom.documentElement.childNodes[1].innerHTML
  }

  cleanNodes(nodes,parent) {
    var nodes = Array.from(nodes)
    nodes.forEach(node => {
      this.cleanNode(node,parent)
    })
  }

  cleanNode(node,parent) {
    if(node.childNodes.length > 0) {
      this.cleanNodes(node.childNodes,node)
    }
    this.cleanAttrs(node)
    if(this.ALLOWED_HTML.includes(node.nodeName.toLowerCase()) === false) {
      parent.removeChild(node)
    }
  }

  cleanAttrs(node) {
    try {
      var attrs = Array.from(node.attributes);
      attrs.forEach(attr => {
        node.attributes.removeNamedItem(attr.name)
      })
    } catch (e) {

    }
  }
}

async function createNote() {
  u = new URLSearchParams(location.search)
  nid = u.get('id');
  r = await fetch('/api/get/'+nid);
  note = await r.json()
  p = new HtmlPurify()
  paste.innerHTML = p.sanitize(note.body);

}


window.onload = () => {
  createNote()
}
