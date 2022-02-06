import { serve } from "https://deno.land/std/http/server.ts";
import * as cookie from "https://deno.land/std/http/cookie.ts";

import * as dejs from "https://deno.land/x/dejs/mod.ts";

const port = 8080;

const handler = async (req: Request): Promise<Response> => {
  let lang = cookie.getCookies(req.headers)["lang"] ?? "en";

  let body = await dejs.renderFileToString("./views/index.ejs", { lang });

  let headers = new Headers();
  headers.set("content-type", "text/html");

  return new Response(body, { headers, status: 200 }); 
};

console.log("[app] server now listening for connections...");
await serve(handler, { port });