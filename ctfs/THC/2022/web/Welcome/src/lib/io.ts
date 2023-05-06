import { io as clientFactory } from 'socket.io-client'

export { type Socket } from 'socket.io-client'

export const io = () => {
  if (!window.socketClient)
    window.socketClient = clientFactory({ path: '/api/socket.io' })
  return window.socketClient
}
