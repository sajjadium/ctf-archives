<script lang="ts" context="module">
  import Contacts from '$lib/Contacts.svelte'
  import Header from '$lib/Header.svelte'
  import Nav from '$lib/Nav.svelte'
  import type { Load } from '@sveltejs/kit'

  export const load: Load = ({ session }) =>
    !session.user?.admin
      ? { redirect: '/', status: 307 }
      : { stuff: { title: 'Find users' } }
</script>

<script lang="ts">
  let name = ''
  let displayName = ''
  let admin: boolean | undefined = undefined

  export let contacts: {
    id: number
    name: string
    displayName: string
    admin: boolean
  }[] = []

  const submit = async () => {
    const where: Record<string, string | boolean> = {}
    if (name) where.name = name
    if (displayName) where.displayName = displayName
    if (admin !== undefined) where.admin = admin

    contacts = await fetch('/api/find-users', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(where),
    }).then((r) => r.json())
  }
</script>

<main>
  <Header>Find users</Header>
  <div class="wrapper">
    <form on:submit|preventDefault={submit}>
      <p>
        <label>
          Name:
          <input type="text" bind:value={name} />
        </label>
      </p>
      <p>
        <label>
          Display name:
          <input type="text" bind:value={displayName} />
        </label>
      </p>
      <p>
        Admin:
        <label>
          <input type="radio" bind:group={admin} value={undefined} /> Any
        </label>
        <label>
          <input type="radio" bind:group={admin} value={true} /> Yes
        </label>
        <label>
          <input type="radio" bind:group={admin} value={false} /> No
        </label>
      </p>
      <p class="center"><button>Search</button></p>
    </form>
    <Contacts {contacts} />
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

  form {
    position: relative;
    padding: 0 1em;
    overflow: hidden;
    background-color: $light-background;
    max-width: 100%;
    border-bottom: 1px solid $border;
    z-index: 1;
  }

  input[type='text'] {
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

  .wrapper {
    flex: 1;
    overflow: auto;
  }

  .center {
    text-align: center;
  }
</style>
