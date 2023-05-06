import { forward } from '$lib/forward'
import type { RequestHandler } from '@sveltejs/kit'

export const get: RequestHandler = async ({ request, params, locals }) => {
  if (!locals.user) return { status: 307, headers: { location: '/register' } }
  const response = await forward(request, `/api/chat/${params.name}`)
  if (!response.ok) return { fallthrough: true }
  return { body: await response.json() }
}
