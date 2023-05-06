import { compile } from './compiler'
import { writeFile as writeFileAsync } from 'fs'
import { promisify } from 'util'

const writeFile = promisify(writeFileAsync)


async function main() {
  let out = Buffer.alloc(8192)
  const cls = compile(`print('hello world')`)
  const size = cls.write(out)
  out = out.slice(0, size)
  await writeFile('Main.class', out)
}

main().catch(e => console.error(e))
