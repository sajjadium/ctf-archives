<script lang="ts" context="module">
  import Contact from '$lib/Contacts.svelte'
  import { io } from '$lib/io'
  import Nav from '$lib/Nav.svelte'
  import type { User } from '@prisma/client'
  import type { Load } from '@sveltejs/kit'
  import { onMount } from 'svelte'

  export const load: Load = ({ props }) => ({
    props,
    stuff: { title: 'Conversations' },
  })
</script>

<script lang="ts">
  export let contacts: {
    id: number
    name: string
    displayName: string
    admin: boolean
  }[] = []

  onMount(() => {
    const socket = io()
    socket.on('message', ({ contact }: { contact: User }) => {
      contacts = [contact, ...contacts.filter((c) => c.id !== contact.id)]
    })
  })
</script>

<main>
  <div class="wrapper">
    <Contact {contacts} />
  </div>

  <Nav />
</main>

<style lang="scss">
  main {
    display: flex;
    flex-direction: column;
    height: 100vh;
    background-color: $background;
  }

  .wrapper {
    flex: 1;
    overflow: auto;
  }
</style>
