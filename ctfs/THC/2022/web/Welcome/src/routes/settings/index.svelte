<script lang="ts" context="module">
  import Header from '$lib/Header.svelte'
  import Nav from '$lib/Nav.svelte'
  import type { User } from '@prisma/client'
  import type { Load } from '@sveltejs/kit'

  export const load: Load = ({ props }) => ({
    props,
    stuff: { title: 'Settings' },
  })
</script>

<script lang="ts">
  export let me: User

  let displayName = me.displayName
  let files: FileList
  let errors: string[] = []
  let success: string | undefined
  let t = String(Date.now())

  const toSentence = (str: string) =>
    (str.at(0) ?? '').toUpperCase() + str.slice(1) + '.'

  // eslint-disable-next-line no-undef
  const submit = async (event: SubmitEvent) => {
    const del = event.submitter?.classList.contains('delete')

    if (del) {
      await fetch('/api/delete-image', { method: 'POST' })
      errors = []
      success = 'profile picture deleted'
      t = String(Date.now())
    } else {
      const response = await fetch('/api/update-name', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ displayName }),
      })
      const body = await response.json()
      errors = []
      success = undefined

      if (!response.ok) {
        errors = body.message.map((message: string) =>
          message.replace(/^displayName/, 'display name'),
        )
      } else {
        success = 'display name updated'
      }
    }
  }

  const submitFile = async () => {
    if (files.length !== 1) return

    const body = new FormData()
    body.append('image', files[0])

    const response = await fetch('/api/update-image', {
      method: 'POST',
      body,
    })
    const responseBody = await response.json()
    errors = []
    success = undefined

    if (!response.ok) {
      errors = responseBody.message
    } else {
      success = 'profile picture updated'
    }
    t = String(Date.now())
  }
</script>

<main>
  <Header>Settings</Header>

  <form on:submit|preventDefault={submit}>
    <div class="contact">
      <label class="image">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          viewBox="0 0 24 24"
          class="edit"
        >
          <path
            d="M12 2c5.514 0 10 4.486 10 10s-4.486 10-10 10-10-4.486-10-10 4.486-10 10-10zm0-2c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm-3.994 12.964l3.106 3.105-4.112.931 1.006-4.036zm9.994-3.764l-5.84 5.921-3.202-3.202 5.841-5.919 3.201 3.2z"
          />
        </svg>
        <img
          src="/api/image?{new URLSearchParams({
            name: me.name,
            accept: 'png,jpg',
            t,
          })}"
          alt="{me.displayName} picture"
          width={64}
          height={64}
        />
        <input
          type="file"
          accept="image/jpeg, image/png"
          bind:files
          on:change={submitFile}
        />
      </label>
      <input
        type="text"
        class="display-name"
        required
        bind:value={displayName}
      />
      <span class="user-name">
        {#if me.admin}
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            class="verified"
          >
            <path
              d="M23.334 11.96c-.713-.726-.872-1.829-.393-2.727.342-.64.366-1.401.064-2.062-.301-.66-.893-1.142-1.601-1.302-.991-.225-1.722-1.067-1.803-2.081-.059-.723-.451-1.378-1.062-1.77-.609-.393-1.367-.478-2.05-.229-.956.347-2.026.032-2.642-.776-.44-.576-1.124-.915-1.85-.915-.725 0-1.409.339-1.849.915-.613.809-1.683 1.124-2.639.777-.682-.248-1.44-.163-2.05.229-.61.392-1.003 1.047-1.061 1.77-.082 1.014-.812 1.857-1.803 2.081-.708.16-1.3.642-1.601 1.302s-.277 1.422.065 2.061c.479.897.32 2.001-.392 2.727-.509.517-.747 1.242-.644 1.96s.536 1.347 1.17 1.7c.888.495 1.352 1.51 1.144 2.505-.147.71.044 1.448.519 1.996.476.549 1.18.844 1.902.798 1.016-.063 1.953.54 2.317 1.489.259.678.82 1.195 1.517 1.399.695.204 1.447.072 2.031-.357.819-.603 1.936-.603 2.754 0 .584.43 1.336.562 2.031.357.697-.204 1.258-.722 1.518-1.399.363-.949 1.301-1.553 2.316-1.489.724.046 1.427-.249 1.902-.798.475-.548.667-1.286.519-1.996-.207-.995.256-2.01 1.145-2.505.633-.354 1.065-.982 1.169-1.7s-.135-1.443-.643-1.96zm-12.584 5.43l-4.5-4.364 1.857-1.857 2.643 2.506 5.643-5.784 1.857 1.857-7.5 7.642z"
            />
            <title>Administrator</title>
          </svg>
        {/if}
        {me.name}
      </span>
    </div>

    {#if success !== undefined}
      <div class="success">{toSentence(success)}</div>
    {/if}

    {#each errors as error}
      <div class="error">{toSentence(error)}</div>
    {/each}

    <p class="center">
      <button type="submit">Save</button>
      <button type="submit" class="delete">Delete profile picture</button>
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

  input[type='file'] {
    display: none;
  }

  button[type='submit'] {
    background-color: $accent;
    border: 0;
    border-radius: 0.5em;
    padding: 0.5em 1em;

    &.delete {
      background: rgb(255, 135, 135);
    }
  }

  .contact {
    position: relative;
    padding: 1em;
    background-color: $light-background;
    display: grid;
    grid-template-columns: 4em 1fr;
    column-gap: 0.5em;
    box-shadow: 0 0 0.25rem $shadow;
    border-radius: 0.5rem;
    margin: 1em 0;
  }

  .image {
    width: 4rem;
    height: 4rem;
    grid-row: 1 / 3;
    position: relative;

    > img {
      width: 4rem;
      height: 4rem;
      border-radius: 50%;
      background: linear-gradient(to bottom, $accent 40%, $shadow);
    }

    .edit {
      position: absolute;
      top: 0;
      right: 0;
      background: $light-background;
      border-radius: 50%;
    }
  }

  .user-name {
    opacity: 0.75;
  }

  .verified {
    width: 1.4em;
    height: 1.4em;
    vertical-align: bottom;
  }

  .center {
    text-align: center;
  }

  .success {
    font-weight: bold;
    color: $success;
  }

  .error {
    font-weight: bold;
    color: $error;
  }
</style>
