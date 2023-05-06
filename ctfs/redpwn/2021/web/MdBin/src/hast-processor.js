import { createElement } from 'react'
import toreact from 'rehype-react'

const dummyUnified = {}
toreact.call(dummyUnified, { createElement })

export const hast2reactCompiler = dummyUnified.Compiler
