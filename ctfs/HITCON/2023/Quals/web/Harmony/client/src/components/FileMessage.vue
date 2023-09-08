<script setup lang="ts">
import { ref } from 'vue'
import { FileContent } from '../common'
import { serverUrl } from '../config'

const props = defineProps<{
	content: FileContent
}>()

const uuidRegex = /^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$/i
const uuid = uuidRegex.test(props.content.uuid) ? props.content.uuid : ''
const fileUrl = new URL(`/file/${uuid}`, serverUrl).href

const imageExts = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']
const isImage = imageExts.some(ext => props.content.filename.toLowerCase().endsWith(ext))
const imgPath = ref<string | null>(null)
if (isImage) {
	window.api.downloadToTemp(fileUrl).then(path => {
		imgPath.value = path
	})
}

const download = () => {
	window.open(fileUrl, '_blank')
}
const copyUrl = () => {
	navigator.clipboard.writeText(fileUrl)
}

</script>
<template>
	<template v-if="isImage">
		<v-img v-if="imgPath" :src="imgPath" cover></v-img>
		<p v-else>Loading...</p>
	</template>
	<template v-else>
		<v-card-text>
			<v-icon icon="mdi-file" size="40"></v-icon>&nbsp;
			<a class="text-h6" :href="fileUrl" target="_blank">{{ content.filename }}</a>
		</v-card-text>
		<v-card-actions>
			<v-btn @click="download">
				Download
			</v-btn>
			<v-btn @click="copyUrl">
				Copy URL
			</v-btn>
		</v-card-actions>
	</template>
</template>
