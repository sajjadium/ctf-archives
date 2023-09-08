<script setup lang="ts">
import { ReceivedMessage } from '../common';
import TextMessage from './TextMessage.vue'
import FileMessage from './FileMessage.vue';

defineProps<{
	message: ReceivedMessage;
}>();
</script>
<template>
	<v-card class="mb-2">
		<template v-slot:title>
			{{ message.sender }}
		</template>

		<template v-slot:subtitle>
			{{ message.time }}
		</template>

		<TextMessage v-if="message.content.type === 'text'" :content="message.content" />
		<FileMessage v-else-if="message.content.type === 'file'" :content="message.content" />
	</v-card>
</template>
