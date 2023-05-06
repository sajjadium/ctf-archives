/** Performs a GET request with the same cookies to another endpoint. */
export const forward = (request: Request, to: string) =>
  fetch(
    new URL(to, `http://localhost:${import.meta.env.VITE_API_PORT}`).toString(),
    {
      headers: { Cookie: request.headers.get('Cookie') ?? '' },
    },
  )
