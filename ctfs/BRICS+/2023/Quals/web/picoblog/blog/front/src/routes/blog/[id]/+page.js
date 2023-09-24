import { goto } from "$app/navigation";
import * as api from "$lib/api";
import { toast } from "@zerodevx/svelte-toast";

/** @type {import('./$types').PageLoad} */
export async function load({ params }) {
  let blog;
  let user;

  try {
    blog = await api.getBlog(params.id, false);
    if (!blog) {
      goto("/");
      return {};
    }

    user = await api.getUser();
  } catch (e) {
    console.log(`Blog retrieval error: ${e}`);
    toast.push(`Failed to get post. Sorry :(`);
    goto("/");
    return {};
  }

  return {
    blog: {
      isAdmin: params.id == user?.blogID,
      id: params.id,
      name: blog.name,
      posts: blog.posts,
    },
  };
}
