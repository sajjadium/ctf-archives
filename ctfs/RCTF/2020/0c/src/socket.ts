import { Socket as NativeSocket, createServer as nativeCreateServer } from 'net'
import { createInterface, Interface } from 'readline'

export function createServer(cb: (socket: Socket) => void) {
  return nativeCreateServer((socket) => cb(new Socket(socket)))
}

export class Socket {
  private rl: Interface
  constructor (public s: NativeSocket) {
    this.rl = createInterface(s)
  }
  writeline(data: string) {
    return new Promise<void>((res, rej) => this.s.write(data + '\n', (err) => {
      if (err) {
        rej(err)
      } else {
        res()
      }
    }))
  }
  readline() {
    return new Promise<string>((res, rej) => {
      this.rl.once('line', res)
      this.rl.once('error', rej)
    })
  }
  close() {
    return new Promise<void>((res) => {
      this.rl.close()
      this.s.destroy()
      res()
    })
  }
}
