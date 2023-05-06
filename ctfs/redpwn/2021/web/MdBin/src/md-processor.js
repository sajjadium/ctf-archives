import unified from 'unified'
import markdown from 'remark-parse'
import remark2rehype from 'remark-rehype'


// This is purely to increase the difficulty of the challenge; no vulns,
// I promise! ~~also ginkoid told me to~~
const stripAttrs = () => {
  const visitor = (node) => {
    if (node.type === 'element' && node.properties != null && typeof node.properties === 'object') {
      let allowedAttrs = []
      if (node.tagName === 'a') {
        allowedAttrs = ['href']
      } else if (node.tagName === 'img') {
        allowedAttrs = ['src']
      }
      for (const prop of Object.keys(node.properties)) {
        if (!allowedAttrs.includes(prop)) {
          delete node.properties[prop]
        }
      }
    }
    node.children?.forEach?.(visitor)
    return node
  }

  return visitor
}

export const markdown2rehype = unified()
  .use(markdown)
  .use(remark2rehype)
  .use(stripAttrs)

export const markdown2hast = markdown =>
  markdown2rehype.runSync(markdown2rehype.parse(markdown))
