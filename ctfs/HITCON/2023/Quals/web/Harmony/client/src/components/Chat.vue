<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { ReceivedMessage, WrappedSocket } from '../common'
import Message from './Message.vue'


const { socket, channel, self } = defineProps<{
	socket: WrappedSocket,
	channel: string,
	self: string
}>()

const messageContainerContainerRef = ref<{ $el: HTMLElement } | null>(null)
const messages = ref<ReceivedMessage[]>([])
const listener = (data: ReceivedMessage) => {
	messages.value.push(data)
	const isAtScrollEndBeforeRender = messageContainerContainerRef.value ? (messageContainerContainerRef.value.$el.scrollTop + messageContainerContainerRef.value?.$el.clientHeight === messageContainerContainerRef.value.$el.scrollHeight) : false
	nextTick(() => {
		if (messageContainerContainerRef.value) {
			const el = messageContainerContainerRef.value.$el

			if (isAtScrollEndBeforeRender || data.sender === self) {
				el.scrollTop = el.scrollHeight
			}
		}
	})
}
onMounted(() => {
	socket.onMessage(listener)
	socket.joinChannel(channel)
})
onUnmounted(() => {
	socket.offMessage(listener)
	socket.leaveChannel(channel)
})

const inputMessage = ref('')
const sendMessage = () => {
	if (!inputMessage.value) return
	socket.sendMessage(channel, {
		type: 'text',
		text: inputMessage.value,
	})
	inputMessage.value = ''
}
const uploadFile = async () => {
	const [fileHandle] = await (<any>window).showOpenFilePicker()
	const file: File = await fileHandle.getFile()
	if (file.size > 1024 * 1024) {
		alert('File too large')
		return
	}
	const buf: ArrayBuffer = await new Promise(resolve => {
		const fr = new FileReader()
		fr.onload = () => resolve(<ArrayBuffer>fr.result)
		fr.readAsArrayBuffer(file)
	})
	const { uuid } = await socket.uploadFile(file.name, buf)
	socket.sendMessage(channel, {
		type: 'file',
		filename: file.name,
		uuid: uuid,
	})
}
</script>
<template>
	<v-container class="container">
		<v-row class="chat-area">
			<v-col :cols="12" class="chat-area-inner" ref="messageContainerContainerRef">
				<Message v-for="m in messages" :key="m.time" :message="m" />
			</v-col>
		</v-row>
		<v-row class="flex-grow-0" style="justify-self: end; height: 100px;">
			<v-col :cols="12">
				<v-text-field v-model="inputMessage" label="Message" append-icon="mdi-send" @click:append="sendMessage"
					@keydown.enter="sendMessage" prepend-icon="mdi-attachment" @click:prepend="uploadFile" required
					autofocus></v-text-field>
			</v-col>
		</v-row>
	</v-container>
</template>
<style scoped>
.container {
	height: calc(100vh - 64px);
	display: flex;
	flex-direction: column;
	justify-content: space-between;
}

.chat-area {
	height: calc(100vh - 64px - 110px);
	max-height: calc(100vh - 64px - 110px);
	flex: 0 0 auto;
}

.chat-area-inner {
	overflow-y: scroll;
	max-height: 100%;
}
</style>
