import DOMPurify from 'dompurify'

DOMPurify.addHook('afterSanitizeAttributes', (node: Element) => {
	if (node instanceof HTMLAnchorElement) {
		node.target = '_blank'
		node.rel = 'noopener noreferrer'
	}
	if (node instanceof HTMLImageElement) {
		node.referrerPolicy = 'no-referrer'
	}
})

export default function sanitize(html: string): DocumentFragment {
	const fragment = DOMPurify.sanitize(html, {
		RETURN_DOM_FRAGMENT: true
	})
	return fragment
}
