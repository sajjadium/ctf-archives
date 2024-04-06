import { forward } from '$lib/forward'
import type { GetSession, Handle } from '@sveltejs/kit'
import { parse } from 'cookie'

export const handle: Handle = async ({ event, resolve }) => {
  event.locals.mobile = Boolean(
    event.request.headers.get('User-Agent')?.toLowerCase().includes('mobile'),
  )
  const { token } = parse(event.request.headers.get('Cookie') ?? '')
  if (token) {
    const response = await forward(event.request, '/api/me')
    if (response.ok) event.locals.user = await response.json()
  }
  return resolve(event)
}

export const getSession: GetSession = ({ locals }) => ({
  mobile: locals.mobile,
  user: locals.user,
})
