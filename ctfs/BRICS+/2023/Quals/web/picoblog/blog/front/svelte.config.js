import adapter from "@sveltejs/adapter-static";

/** @type {import('@sveltejs/kit').Config} */
const config = {
  kit: {
    // adapter-auto only supports some environments, see https://kit.svelte.dev/docs/adapter-auto for a list.
    // If your environment is not supported or you settled on a specific environment, switch out the adapter.
    // See https://kit.svelte.dev/docs/adapters for more information about adapters.
    adapter: adapter({
      fallback: "index.html",
    }),
    csp: {
      directives: {
        "default-src": [
          "self",
          "https://picoblog-static-ae182846340bc2df.brics-ctf.ru",
        ],
        "font-src": ["fonts.gstatic.com"],
        "style-src": ["self", "fonts.googleapis.com"],
        "object-src": ["none"],
      },
      mode: "hash",
    },
  },
};

export default config;
