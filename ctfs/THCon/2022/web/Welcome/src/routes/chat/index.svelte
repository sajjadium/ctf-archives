<script lang="ts" context="module">
  import { goto } from '$app/navigation'
  import Header from '$lib/Header.svelte'
  import Nav from '$lib/Nav.svelte'
  import type { Load } from '@sveltejs/kit'

  export const load: Load = ({ session }) =>
    session.user
      ? {
          stuff: {
            title: 'New Conversation',
          },
        }
      : { status: 307, redirect: '/register' }
</script>

<script lang="ts">
  let name = ''
  let error: string | undefined

  export const submit = async () => {
    const response = await fetch(`/api/user/${encodeURIComponent(name)}`)
    error = undefined
    if (!response.ok) {
      error = 'User not found.'
      return
    }
    await goto(`/chat/${encodeURIComponent(name)}`)
  }
</script>

<main>
  <Header>New conversation</Header>
  <form on:submit|preventDefault={submit}>
    <p>
      <label>To <input type="text" bind:value={name} /></label>
    </p>
    {#if error}
      <div class="error">{error}</div>
    {/if}
    <p class="center">
      <button>Open conversation</button>
    </p>
  </form>
  <Nav />
</main>

<style lang="scss">
  main {
    display: flex;
    flex-direction: column;
    height: 100vh;
    background-color: $background;
  }

  form {
    flex: 1;
    overflow: auto;
    background: $light-background;
    padding: 0 1em;
  }

  input {
    width: 100%;
    border-radius: 0.5em;
    border-color: $border;
  }

  button {
    background-color: $accent;
    border: 0;
    border-radius: 0.5em;
    padding: 0.5em 1em;
  }

  .center {
    text-align: center;
  }

  .error {
    font-weight: bold;
    color: $error;
  }
</style>
