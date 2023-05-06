import { forward } from '$lib/forward'
import type { RequestHandler } from '@sveltejs/kit'

export const get: RequestHandler = async ({ request, locals }) =>
  locals.user
    ? {
        body: {
          me: await forward(request, '/api/me').then((r) => r.json()),
        },
      }
    : { status: 307, headers: { location: '/register' } }
