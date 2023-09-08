<script setup lang="ts">
import Chat from './components/Chat.vue'
import LoginForm from './components/LoginForm.vue'
import { ref, onMounted } from 'vue'
import socketio from 'socket.io-client'
import { Auth, WrappedSocket } from './common'
import { serverUrl, defaultChannel } from './config'

const drawer = ref(false)

const channels = ref<string[]>([defaultChannel])
const currentChannel = ref<string>(defaultChannel)
const joinChannel = async () => {
	const channel = typeof window.api !== 'undefined' ? (await window.api.prompt('Channel Name')) : prompt('Channel Name')
	if (!channel) return
	if (!channels.value.includes(channel)) {
		channels.value.push(channel)
	}
	currentChannel.value = channel

	if (typeof window.api !== 'undefined' && auth.value) {
		window.api.setChannels(auth.value.username, {
			[channel]: true
		})
	}
}
const leaveChannel = (channel: string) => {
	channels.value = channels.value.filter(c => c !== channel)
	if (currentChannel.value === channel) {
		currentChannel.value = defaultChannel
	}
	if (typeof window.api !== 'undefined' && auth.value) {
		window.api.setChannels(auth.value.username, {
			[channel]: false
		})
	}
}


const auth = ref<Auth | null>(null)
let socket: WrappedSocket | null = null

onMounted(async () => {
	if (typeof window.api !== 'undefined') {
		const ret = await window.api.getAuth()
		if (ret) {
			logined(ret)
		}
	}
})

const logined = async (receivedAuth: Auth) => {
	auth.value = receivedAuth
	socket = new WrappedSocket(socketio(serverUrl, {
		auth: {
			username: receivedAuth.username,
			password: receivedAuth.password,
		}
	}))
	if (typeof window.api !== 'undefined') {
		window.api.setAuth(receivedAuth)
		const ret = await window.api.getChannels(receivedAuth.username)
		if (ret) {
			channels.value = Object.entries(ret).filter(([_, v]) => v).map(([k, _]) => k).sort()
		}
	}
}

const logout = () => {
	auth.value = null
	if (typeof window.api !== 'undefined') {
		window.api.setAuth(undefined)
	}
}
</script>

<template>
	<v-app theme="dark">
		<v-app-bar>
			<v-app-bar-nav-icon variant="text" @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
			<v-toolbar-title v-if="auth">Harmony - #{{ currentChannel }}</v-toolbar-title>
			<v-toolbar-title v-else>Harmony - Login</v-toolbar-title>
			<template v-slot:append>
				<v-btn v-if="auth" icon="mdi-logout" @click="logout"></v-btn>
			</template>
		</v-app-bar>
		<v-navigation-drawer v-model="drawer" temporary>
			<v-list-item v-if="!auth" title="Please Login First" prepend-icon="mdi-information"></v-list-item>
			<template v-else>
				<v-list-item title="Join Channel" prepend-icon="mdi-plus" @click="joinChannel"></v-list-item>
				<v-list-item v-for="c in channels" :key="c" :title="'#' + c" prepend-icon="mdi-message"
					@click="drawer = false; currentChannel = c">

					<template v-slot:append>
						<v-icon icon="mdi-close" variant="text" @click.stop="leaveChannel(c)"></v-icon>
					</template>
				</v-list-item>
			</template>
		</v-navigation-drawer>
		<v-main>
			<LoginForm v-if="!auth" :server-url="serverUrl" @logined="logined" />
			<Chat :key="currentChannel" :socket="socket!" :channel="currentChannel!" :self="auth.username" v-else />
		</v-main>
	</v-app>
</template>
