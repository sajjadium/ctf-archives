<script setup lang="ts">
import { TextContent } from '../common'
import { ref, onMounted } from 'vue'
import sanitize from '../dompurify'
import { marked } from 'marked'

const contentEl = ref<HTMLElement | null>(null)
const props = defineProps<{
	content: TextContent
}>()

function getYoutubeEmbedUrl(url: string): string | null {
	// known youtube url formats
	// https://www.youtube.com/watch?v=hI34Bhf5SaY
	// https://youtu.be/w4U9S5eX3eY
	// https://m.youtube.com/watch?v=kv4UD4ICd_0
	// https://music.youtube.com/watch?v=GL5s27qtvWw
	// https://www.youtube.com/v/ZK64DWBQNXw
	// https://m.youtube.com/v/dQw4w9WgXcQ
	// https://www.youtube.com/e/F5GjEwI8wEA
	// https://m.youtube.com/e/4daUOEfnYKI
	const parsed = new URL(url)
	if (parsed.hostname === 'youtu.be') {
		parsed.hostname = 'www.youtube.com'
		parsed.pathname = `/embed${parsed.pathname}`
		return parsed.href
	}
	const ythost = /\w+\.youtube\.com/
	if (!ythost.test(parsed.hostname)) {
		return null
	}
	parsed.hostname = parsed.hostname.replace(ythost, 'www.youtube.com')
	if (parsed.pathname === '/watch') {
		parsed.pathname = `/embed/${parsed.searchParams.get('v')}`
		parsed.search = ''
		return parsed.href
	}
	if (parsed.pathname.startsWith('/v/') || parsed.pathname.startsWith('/e/')) {
		parsed.pathname = `/embed/${parsed.pathname.slice(3)}`
		parsed.search = ''
		return parsed.href
	}
	return null
}

onMounted(() => {
	const html = marked.parse(props.content.text, {
		headerIds: false,
		mangle: false
	})
	const frag = sanitize(html)
	for (const node of frag.querySelectorAll('a')) {
		// try to convert youtube links to embedded videos
		// we only convert empty links or links with the same text content
		// the latter happens when the link is automatically converted by marked
		if (node.textContent && node.textContent != node.href) continue
		console.log("href", node.href)
		const embedUrl = getYoutubeEmbedUrl(node.href)
		if (embedUrl) {
			const iframe = document.createElement('iframe')
			iframe.width = '560'
			iframe.height = '315'
			iframe.allowFullscreen = true
			iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture'
			iframe.referrerPolicy = 'no-referrer'
			iframe.sandbox.add('allow-presentation')
			iframe.sandbox.add('allow-popups')
			iframe.sandbox.add('allow-scripts')
			iframe.sandbox.add('allow-same-origin')
			iframe.src = embedUrl
			node.replaceWith(iframe)
		}
	}
	contentEl.value!.appendChild(frag)
})
</script>
<template>
	<v-card-text>
		<div ref="contentEl"></div>
	</v-card-text>
</template>
