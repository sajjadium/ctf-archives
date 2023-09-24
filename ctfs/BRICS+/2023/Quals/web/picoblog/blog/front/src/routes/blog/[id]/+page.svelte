<script>
  import * as api from "$lib/api";
  import { toast } from "@zerodevx/svelte-toast";

  let title = "";
  let content = "";

  async function createPost() {
    try {
      await api.createPost(title, content);

      if (data.blog) {
        const blog = await api.getBlog(data.blog.id, true);
        data.blog.posts = blog?.posts || data.blog.posts;
      }
    } catch (e) {
      console.log(`Post creation error: ${e}`);
      toast.push(`Failed to create new post. Sorry :(`);
    }
  }

  async function askForReview() {
    try {
      await api.askForReview();
    } catch (e) {
      console.log(`Review error: ${e}`);
      toast.push(`Failed to review your blog. Sorry :(`);
    }
  }

  /** @type {import('./$types').PageData} */
  export let data;
</script>

<nav>
  <h1 class="tc ma0 mb3 f-subheadline serif-title">
    <a class="link black dim" href="/blog/{data.blog?.id}">{data.blog?.name}</a>
  </h1>
  {#if data.blog?.isAdmin}
    <a class="tc link navy db dim serif-text" on:click={askForReview} href="#/"
      >Review my blog</a
    >
  {/if}
</nav>

<div class="pt3 flex flex-column items-center serif-text">
  {#if data.blog?.isAdmin}
    <form on:submit={createPost} class="post-form mb3 flex flex-column">
      <input
        id="title"
        type="text"
        class="input-reset mb3 pa1 ph2 ba br1 b--moon-gray f4"
        placeholder="Title"
        bind:value={title}
        required
        maxlength="100"
      />
      <textarea
        class="input-reset mb3 pa2 ba br1 b--moon-gray"
        bind:value={content}
        required
        maxlength="256"
        placeholder="Post markup..."
      />
      <button
        class="link black bg-near-white ba br1 b--moon-gray grow ph4 pv3 b f3"
        >Post something</button
      >
    </form>
  {/if}
  {#each data.blog?.posts || [] as post}
    <article>
      <h1 class="measure f1 serif-title">{post.title}</h1>
      <p class="measure-wide lh-copy">{@html post.content}</p>
    </article>
  {/each}
</div>

<style>
  nav {
    margin: 3rem 0;
  }

  div {
    gap: 3rem;
  }

  .post-form {
    width: 32rem;
  }

  article {
    overflow-wrap: anywhere;
    width: 34em;
  }
</style>
