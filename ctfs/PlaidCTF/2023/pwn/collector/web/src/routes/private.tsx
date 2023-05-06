import { Show, Suspense } from "solid-js";
import { FormError, Navigate, useRouteData } from "solid-start";
import { createServerAction$, createServerData$, redirect } from "solid-start/server"

export function routeData() {
  return createServerData$(async () => {
    const url = process.env.SLINGSHOT_URL;
    if (url) return redirect(url);
    return 'unsupported';
  })
}

export default function Private() {
  const data = useRouteData<typeof routeData>();
  return (
    <main>
      <Show when={!data.loading} fallback={"Loading..."}>
        <Show when={data() === 'unsupported'} fallback={<Navigate href="/" />}>
          Private instances are not supported
        </Show>
      </Show>
    </main>
  );
}