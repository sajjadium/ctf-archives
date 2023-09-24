<script>
  import { SvelteToast } from "@zerodevx/svelte-toast";
</script>

<SvelteToast
  options={{
    classes: ["serif-text"],
  }}
/>

<slot />
