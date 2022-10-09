<script>
  // @ts-nocheck
  import {
    buildDefaultSettings,
    parseQueryString,
    combineSettings,
    extractSettings,
  } from "../helpers/utils";

  let defaultSettings = buildDefaultSettings();
  const queryObj = parseQueryString(window.location.search);
  const userSettings = JSON.parse(extractSettings(queryObj));
  defaultSettings = combineSettings(defaultSettings, userSettings);
</script>

<svelte:head>
  <title>{defaultSettings.title}</title>
  <meta name="robots" content={defaultSettings.meta.robots} />
  <meta name="description" content={defaultSettings.meta.description} />
  <meta name="keywords" content={defaultSettings.meta.keywords} />
</svelte:head>

<div>
  <!-- heading/subheading text -->
  {#each Object.entries($$props) as [key, value]}
    {#if key === "heading"}
      <h1>{value}</h1>
    {:else if key === "subheading"}
      <h3>{value}</h3>
    {:else}
      {@html value}
    {/if}
  {/each}
</div>
