<script lang="ts">
  import { page, session } from '$app/stores'
  import '../app.scss'
</script>

<svelte:head>
  <title>
    {$page.stuff.title ? `${$page.stuff.title} – ` : ''}Bastion
  </title>
  <meta name="description" content={$page.stuff.title} />
</svelte:head>

{#if $session.mobile}
  <slot />
{:else}
  <main>
    <h1>Please use Bastion on your phone.</h1>
    <h2>
      The desktop version is currently in
      pre-alpha-insider-limited-turbo-private phase.
    </h2>
  </main>
{/if}

<style lang="scss">
  main {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    min-height: 100vh;
    background-color: $background;
    padding: 1em;
  }

  h2 {
    font-weight: inherit;
    opacity: 0.8;
  }
</style>
