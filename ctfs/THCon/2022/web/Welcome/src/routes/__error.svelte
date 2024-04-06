<script lang="ts" context="module">
  import type { ErrorLoad } from '@sveltejs/kit'

  export const load: ErrorLoad = ({ error, status }) => {
    return {
      stuff: { title: 'Error' },
      props: { error, status },
    }
  }
</script>

<script lang="ts">
  export let error: Error | undefined
  export let status: number | undefined
</script>

<main>
  <div>
    <h1>{status}</h1>
    <p>{error?.message}</p>
  </div>
</main>

<style lang="scss">
  main {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: $background;
  }

  div {
    padding: 1em 2em;
    background-color: $light-background;
    border-radius: 1em;
    box-shadow: 0 1em 2em $shadow;
    width: 400px;
    max-width: 100%;
    margin: 0.5em;
  }
</style>
