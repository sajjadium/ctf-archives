<h1>
  <a href="/" sveltekit:prefetch>
    <svg width="24" height="24" xmlns="http://www.w3.org/2000/svg">
      <path
        d="M20 .755l-14.374 11.245 14.374 11.219-.619.781-15.381-12 15.391-12 .609.755z"
      />
    </svg>
  </a>
  <slot />
</h1>

<style lang="scss">
  h1 {
    margin: 0;
    padding: 1rem;
    background: $light-background;
    border-bottom: 1px solid $border;

    > a {
      margin-right: 0.5rem;
      color: inherit;
    }
  }

  svg {
    vertical-align: baseline;
  }
</style>
