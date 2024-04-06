<script lang="ts" context="module">
  import { goto } from '$app/navigation'
  import { session } from '$app/stores'
  import type { Load } from '@sveltejs/kit'

  export const load: Load = ({ session }) =>
    session.user
      ? { redirect: '/', status: 307 }
      : { stuff: { title: 'Register' } }
</script>

<script lang="ts">
  let name = ''
  let displayName = ''
  let errors: { [x: string]: string[] } = {
    name: [],
    displayName: [],
  }

  const toSentence = (str: string) =>
    (str.at(0) ?? '').toUpperCase() + str.slice(1) + '.'

  const submit = async () => {
    const response = await fetch('/api/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name, displayName }),
    })
    const body = await response.json()
    errors = {
      name: [],
      displayName: [],
    }

    if (!response.ok) {
      const messages: string[] = body?.message ?? []
      for (const message of messages) {
        const index = message.indexOf(' ')
        var [scope, details] = [
          message.slice(0, index),
          message.slice(index + 1),
        ]
        errors[scope].push(details)
      }
      // Trigger Svelte refresh
      errors = errors
      return
    }

    // Prevent client-side redirection to '/register'
    $session.user = body
    const { token } = body
    document.cookie = `token=${token}; path=/; max-age=31536000`
    await goto('/')
  }
</script>

<main>
  <form on:submit|preventDefault={submit}>
    <h1>Register</h1>
    <p>
      <label>
        Username<br />
        <input type="text" required bind:value={name} />
      </label>
      {#each errors.name as error}
        <div class="error">{toSentence(error)}</div>
      {/each}
    </p>
    <p>
      <label>
        Dislay name<br />
        <input type="text" required bind:value={displayName} />
      </label>
      {#each errors.displayName as error}
        <div class="error">{toSentence(error)}</div>
      {/each}
    </p>
    <p class="center"><button>Register</button></p>
  </form>
</main>

<style lang="scss">
  main {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: $background;
  }

  form {
    padding: 1em 2em;
    background-color: $light-background;
    border-radius: 1em;
    box-shadow: 0 1em 2em $shadow;
    width: 400px;
    max-width: 100%;
    margin: 0.5em;
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
