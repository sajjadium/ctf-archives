<script>
  import { goto } from "$app/navigation";
  import * as api from "$lib/api";
  import { toast } from "@zerodevx/svelte-toast";

  let name = "";

  async function createBlog() {
    try {
      const blogID = await api.createBlog(name);
      goto(`/blog/${blogID}`);
    } catch (e) {
      console.log(`Blog creation error: ${e}`);
      toast.push(`Failed to create new blog. Sorry :(`);
    }
  }
</script>

<nav class="pa3 pt4">
  <h1 class="tc f2 serif-title">
    <a class="link black dim" href="/">picoblog</a>
  </h1>
</nav>

<div class="flex flex-column items-center serif-text">
  <p class="tc measure-narrow lh-copy f4">
    Simple and minimalistic microblogging without any censorship. Ever.
  </p>
  <form on:submit={createBlog} class="flex flex-column">
    <input
      id="name"
      type="text"
      class="input-reset mb3 pa1 ph2 ba br1 b--moon-gray f4"
      placeholder="Name"
      required
      maxlength="100"
      bind:value={name}
    />
    <button
      class="link black bg-near-white ba br1 b--moon-gray grow ph4 pv3 b f3"
      >Start a blog</button
    >
  </form>
</div>

<style>
  div {
    gap: 5rem;
  }
</style>
