<script setup lang="ts">
import { ref } from 'vue'
import xf, { HTTPError } from 'xfetch-js'
import { Auth } from '../common'

const props = defineProps<{
	serverUrl: string
}>()

const emit = defineEmits({
	logined: (__: Auth) => true,
})

const username = ref('')
const password = ref('')
const errorMessage = ref('')

const client = xf.extend({
	baseURI: props.serverUrl,
})

const register = async () => {
	try {
		await client.post('/register', {
			json: {
				username: username.value,
				password: password.value,
			},
		})
	}
	catch (e) {
		errorMessage.value = (await (<typeof HTTPError>e).response.json()).error
	}
}
const login = async () => {
	try {
		await client.post('/login', {
			json: {
				username: username.value,
				password: password.value,
			},
		})
		emit('logined', {
			username: username.value,
			password: password.value,
		})
	}
	catch (e) {
		errorMessage.value = (await (<typeof HTTPError>e).response.json()).error
	}
}
</script>
<template>
	<v-form>
		<v-container>
			<v-alert v-if="errorMessage" density="compact" type="warning" title="Error" :text="errorMessage"></v-alert>
			<v-row justify="center">
				<v-col :cols="6">
					<v-text-field v-model="username" label="Username" required></v-text-field>
				</v-col>
			</v-row>
			<v-row justify="center">
				<v-col :cols="6">
					<v-text-field v-model="password" label="Password" type="password" required
						@keydown.enter="login"></v-text-field>
				</v-col>
			</v-row>
			<v-row justify="center">
				<v-col :cols="6">
					<v-btn color="primary" @click="login">Login</v-btn>
					<v-btn color="secondary" @click="register" class="ml-2">Register</v-btn>
				</v-col>
			</v-row>
		</v-container>
	</v-form>
</template>
