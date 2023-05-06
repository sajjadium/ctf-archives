import { Socket } from './socket'
import { createHash } from 'crypto'

function sha256(data: string): string {
  const hash = createHash('sha256')
  hash.update(data, 'utf8')
  return hash.digest().toString('hex')
}

function randomString(size: number, from: string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') {
  let out = ''
  for (let i = 0; i < size; i++) {
    out += from[Math.floor(Math.random() * from.length)]
  }
  return out
}

function generateChallenge(difficulty: number = 16) {
  const full = randomString(20)
  const [display, hidden] = [full.slice(0, difficulty), full.slice(difficulty)]
  return [
    `sha256('${display}' + '${'?'.repeat(hidden.length)}') == '${sha256(full)}'`,
    hidden
  ] as const
}

export function checkPow(next: (socket: Socket) => Promise<void>) {
  return async (socket: Socket) => {
    const [ challenge, hidden ] = generateChallenge()
    console.log('challenge', challenge, hidden)
    await socket.writeline(challenge)
    const ans = await socket.readline()
    if (hidden === ans) {
      return next(socket)
    } else {
      await socket.writeline(`Wrong answer, the answer is ${hidden}`)
      await socket.close()
    }
  }
}
