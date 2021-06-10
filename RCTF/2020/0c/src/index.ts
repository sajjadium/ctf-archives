import { compile } from './compiler'
import { Socket, createServer } from './socket'
import { checkPow } from './pow'
import { Stream } from 'stream'
import { pack } from 'tar-stream'
import pLimit from 'p-limit'
import Docker from 'dockerode'

const Timeout = 1 * 1000 // 1s
const CodeLocation = '/data'
const DockerTag = 'openjdk:8-alpine'
const limit = pLimit(5)
const docker = new Docker()

function getStream(stream: Stream) {
  return new Promise<string>((resolve, reject) => {
    let out: Buffer[] = []
    const end = () => resolve(Buffer.concat(out).toString())
    stream.on('data', buf => out.push(buf))
    stream.on('end', end)
    stream.on('error', err => reject(err))
  })
}

function startContainerWithTimeout(container: Docker.Container) {
  return new Promise<string>(async (resolve, reject) => {
    let stop = false
    setTimeout(() => {
      stop = true
      reject(new Error('Timeout'))
      container.kill().catch(e => void 0)
    }, Timeout)
    try {
      const stream = await container.attach({
        stream: true,
        stdout: true,
        stderr: true,
        tty: true,
      })
      await container.start()
      if (stop) return
      await container.wait()
      resolve(getStream(stream))
      if (stop) return
    } catch(e) {
      reject(e)
    }
  })
}

async function onConnection(socket: Socket) {
  await socket.writeline(`Welcome to c0 online demo!`)
  await socket.writeline(`Zero-featured TypeScript on JVM\n`)
  await socket.writeline(`You can input your code and see the result!`)
  await socket.writeline(`For example:
print('hello world')
`)
  await socket.writeline(`Code(end with empty line):`)
  const code = []
  for (let i = 0; i < 50; i++) {
    const line = await socket.readline()
    if (line === '') break
    code.push(line)
  }

  let out = Buffer.alloc(8192)
  const cls = compile(code.join('\n'))
  const size = cls.write(out)
  out = out.slice(0, size)
  await socket.writeline(`Compile complete, size: ${out.byteLength}`)

  if (limit.pendingCount > 0) {
    await socket.writeline('Queuing...')
  }
  await limit(async () => {
    const tar = pack()
    tar.entry({ name: 'Main.class' }, out)
    tar.finalize()

    await socket.writeline('Running...')
    const c = await docker.createContainer({
      Image: DockerTag,
      Cmd: ['java', 'Main', '-Xms32m', 'Xmx64m'],
      Env: [`FLAG=${process.env.FLAG}`],
      WorkingDir: CodeLocation,
      Tty: true,
      HostConfig: {
        AutoRemove: true
      },
    })
    await c.putArchive(tar, { path: CodeLocation })
    const result = await startContainerWithTimeout(c)
    await socket.writeline('Result:')
    await socket.writeline(result)
  })
  await socket.writeline('Bye!')
}

function asyncWrapper(cb: (socket: Socket) => Promise<void>) {
  return async (socket: Socket) => {
    try {
      await cb(socket)
    } catch (e) {
      console.error(e)
      await socket.writeline(`Error: ${e.message}`)
    } finally {
      await socket.close()
    }
  }
}

async function main() {
  try {
    await docker.run(DockerTag, ['java', '-version'], process.stdout, {
      HostConfig: {
        AutoRemove: true
      }
    })
  } catch (e) {
    console.log('Pulling docker image')
    await docker.pull(DockerTag, {})
  }
  const server = createServer(
    asyncWrapper(checkPow(onConnection))
  )
  const host = process.env.HOST ?? '127.0.0.1'
  const port = process.env.PORT ?? '5000'
  server.listen(parseInt(port), host)
  console.log(`Server ready at ${host}:${port}`)
}

main().catch(e => console.error(e))
