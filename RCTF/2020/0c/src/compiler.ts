import { createSourceFile, ScriptTarget, SyntaxKind, VariableStatement, Identifier, StringLiteral, NumericLiteral, ExpressionStatement, CallExpression, Expression, BinaryExpression } from 'typescript'
import { equal } from 'assert'

enum ConstantKind {
  TAG_CLASS = 7,
  TAG_FIELD_REF = 9,
  TAG_METHOD_REF = 10,
  TAG_INTERFACE_METHOD_REF = 11,
  TAG_STRING = 8,
  TAG_INTEGER = 3,
  TAG_FLOAT = 4,
  TAG_LONG = 5,
  TAG_DOUBLE = 6,
  TAG_NAME_AND_TYPE = 12,
  TAG_UTF8 = 1,
  TAG_METHOD_HANDLE = 15,
  TAG_METHOD_TYPE = 16,
  TAG_INVOKE_DYNAMIC = 18,
}
enum AccessFlags {
  Public = 1,
  StaticPublic = 9,
}

type Constant = {
  kind: ConstantKind.TAG_UTF8
  str: string
} | {
  kind: ConstantKind.TAG_DOUBLE
  num: number
} | {
  kind: ConstantKind.TAG_CLASS
  name_index: number
} | {
  kind: ConstantKind.TAG_METHOD_REF
  class_index: number
  name_and_type_index: number
} | {
  kind: ConstantKind.TAG_NAME_AND_TYPE
  name_index: number
  description_index: number
} | {
  kind: ConstantKind.TAG_FIELD_REF
  class_index: number
  name_and_type_index: number
} | {
  kind: ConstantKind.TAG_STRING
  string_index: number
}
class ConstantPool {
  pool: Constant[] = []
  constructor () {}
  addString(str: string) {
    const existed = this.pool.findIndex(i => i.kind === ConstantKind.TAG_UTF8 && i.str === str) + 1
    if (existed) {
      return existed
    }
    this.pool.push({
      kind: ConstantKind.TAG_UTF8,
      str
    })
    return this.pool.length
  }
  addStringObj(string_index: number) {
    const existed = this.pool.findIndex(i => i.kind === ConstantKind.TAG_STRING && i.string_index === string_index) + 1
    if (existed) {
      return existed
    }
    this.pool.push({
      kind: ConstantKind.TAG_STRING,
      string_index
    })
    return this.pool.length
  }
  addNumber(num: number) {
    const existed = this.pool.findIndex(i => i.kind === ConstantKind.TAG_DOUBLE && i.num === num) + 1
    if (existed) {
      return existed
    }
    this.pool.push({
      kind: ConstantKind.TAG_DOUBLE,
      num
    })
    return this.pool.length
  }
  addClass(name_index: number) {
    const existed = this.pool.findIndex(i => i.kind === ConstantKind.TAG_CLASS && i.name_index === name_index) + 1
    if (existed) {
      return existed
    }
    this.pool.push({
      kind: ConstantKind.TAG_CLASS,
      name_index
    })
    return this.pool.length
  }
  addMethodRef(class_index: number, name_and_type_index: number) {
    const existed = this.pool.findIndex(i => i.kind === ConstantKind.TAG_METHOD_REF
      && i.class_index === class_index
      && i.name_and_type_index === name_and_type_index
    ) + 1
    if (existed) {
      return existed
    }
    this.pool.push({
      kind: ConstantKind.TAG_METHOD_REF,
      class_index,
      name_and_type_index
    })
    return this.pool.length
  }
  addNameAndType(name_index: number, description_index: number) {
    const existed = this.pool.findIndex(i => i.kind === ConstantKind.TAG_NAME_AND_TYPE
      && i.name_index === name_index
      && i.description_index === description_index
    ) + 1
    if (existed) {
      return existed
    }
    this.pool.push({
      kind: ConstantKind.TAG_NAME_AND_TYPE,
      name_index,
      description_index
    })
    return this.pool.length
  }
  addFieldRef(class_index: number, name_and_type_index: number) {
    const existed = this.pool.findIndex(i => i.kind === ConstantKind.TAG_FIELD_REF
      && i.class_index === class_index
      && i.name_and_type_index === name_and_type_index
    ) + 1
    if (existed) {
      return existed
    }
    this.pool.push({
      kind: ConstantKind.TAG_FIELD_REF,
      class_index,
      name_and_type_index
    })
    return this.pool.length
  }
  getMethodRef(cls: string, name: string, description: string) {
    return this.addMethodRef(
      this.addClass(this.addString(cls)),
      this.addNameAndType(
        this.addString(name),
        this.addString(description)
      )
    )
  }
  getFieldRef(cls: string, name: string, description: string) {
    return this.addFieldRef(
      this.addClass(this.addString(cls)),
      this.addNameAndType(this.addString(name), this.addString(description))
    )
  }
  write(buffer: Buffer, offset: number = 8) {
    offset = buffer.writeUInt16BE(this.pool.length + 1, offset)
    for (const c of this.pool) {
      offset = buffer.writeUInt8(c.kind, offset)
      switch (c.kind) {
        case ConstantKind.TAG_UTF8:
          offset = buffer.writeUInt16BE(c.str.length, offset)
          offset += buffer.write(c.str, offset, 'utf-8')
          break
        case ConstantKind.TAG_DOUBLE:
          offset = buffer.writeDoubleBE(c.num, offset)
          break
        case ConstantKind.TAG_CLASS:
          offset = buffer.writeUInt16BE(c.name_index, offset)
          break
        case ConstantKind.TAG_METHOD_REF:
          offset = buffer.writeUInt16BE(c.class_index, offset)
          offset = buffer.writeUInt16BE(c.name_and_type_index, offset)
          break
        case ConstantKind.TAG_NAME_AND_TYPE:
          offset = buffer.writeUInt16BE(c.name_index, offset)
          offset = buffer.writeUInt16BE(c.description_index, offset)
          break
        case ConstantKind.TAG_FIELD_REF:
          offset = buffer.writeUInt16BE(c.class_index, offset)
          offset = buffer.writeUInt16BE(c.name_and_type_index, offset)
          break
        case ConstantKind.TAG_STRING:
          offset = buffer.writeUInt16BE(c.string_index, offset)
          break
        default:
          // @ts-ignore
          throw new TypeError(`ConstantKind: ${c.kind} is not supported`)
      }
    }

    return offset
  }
}

class ClassInfo {
  pool = new ConstantPool()
  thisClass = 'Main'
  superClass = 'java/lang/Object'
  main?: Buffer
  template = this.makeTemplate()
  constructor() {}
  makePrint() {
    const buf = Buffer.from([
      0xB2, // getstatic
      0, 0, // field ref
      0x2A, // aload_0
      0xB6, // invoke_virtual
      0, 0, // method ref
      0xB1, // return
    ])
    const p = this.pool
    buf.writeUInt16BE(p.getFieldRef(
      'java/lang/System', 'out', 'Ljava/io/PrintStream;'
    ), 1)
    buf.writeUInt16BE(p.getMethodRef(
      'java/io/PrintStream', 'println', '(Ljava/lang/String;)V'
    ), 5)
    return buf
  }
  makeCodeAttr(code: Buffer) {
    const buf = Buffer.alloc(1024)
    let offset = 0
    offset = buf.writeUInt16BE(0x10, offset) // max stack
    offset = buf.writeUInt16BE(0x10, offset) // max locals
    offset = buf.writeUInt32BE(code.byteLength, offset) // code length
    offset += code.copy(buf, offset) // code
    offset = buf.writeUInt16BE(0, offset) // exception table length
    offset = buf.writeUInt16BE(0, offset) // attr length
    return buf.slice(0, offset)
  }
  makeMethodInfo(access: AccessFlags, name: string, description: string, code: Buffer) {
    const buf = Buffer.alloc(1024)
    let offset = 0
    offset = buf.writeUInt16BE(access, offset) // access
    offset = buf.writeUInt16BE(this.pool.addString(name), offset) // name
    offset = buf.writeUInt16BE(this.pool.addString(description), offset) // description
    offset = buf.writeUInt16BE(1, offset) // attr count

    const codeAttr = this.makeCodeAttr(code)
    offset = buf.writeUInt16BE(this.pool.addString('Code'), offset) // Code attribute
    offset = buf.writeUInt32BE(codeAttr.byteLength, offset) // attr length
    offset += codeAttr.copy(buf, offset)
    return buf.slice(0, offset)
  }
  makeTemplate() {
    const p = this.pool
    const thisClass = p.addClass(p.addString(this.thisClass))
    const superClass = p.addClass(p.addString(this.superClass))
    const printMI = this.makeMethodInfo(AccessFlags.StaticPublic, 'print', '(Ljava/lang/String;)V', this.makePrint())

    return {
      thisClass,
      superClass,
      printMI,
    }
  }
  write(buffer: Buffer) {
    if (!this.main) {
      throw new TypeError(`Main code is not set`)
    }
    const {
      thisClass,
      superClass,
      printMI,
    } = this.template
    const main = this.makeMethodInfo(AccessFlags.StaticPublic, 'main', '([Ljava/lang/String;)V', this.main)
    const methods: Buffer[] = [printMI, main]

    let offset = 0
    offset = buffer.writeUInt32BE(0xcafebabe, offset)
    offset = buffer.writeUInt16BE(0, offset)
    offset = buffer.writeUInt16BE(52, offset)
    offset = this.pool.write(buffer, offset)
    offset = buffer.writeUInt16BE(0x21, offset) // access flags: SUPER,PUBLIC
    offset = buffer.writeUInt16BE(thisClass, offset) // this class
    offset = buffer.writeUInt16BE(superClass, offset) // super class
    offset = buffer.writeUInt16BE(0, offset) // interface count
    offset = buffer.writeUInt16BE(0, offset) // fields count
    offset = buffer.writeUInt16BE(methods.length, offset) // methods count
    // methods
    for (const m of  methods) {
      offset += m.copy(buffer, offset)
    }
    // methods end
    offset = buffer.writeUInt16BE(0, offset) // attr count

    return offset
  }
}

class Assembler {
  private offset = 0
  private p = this.cls.pool
  constructor (private buf: Buffer, private cls: ClassInfo) {}
  pushConstant(index: number) {
    this.offset = this.buf.writeUInt8(0x13, this.offset) // ldc_w
    this.offset = this.buf.writeUInt16BE(index, this.offset)
  }
  pushVariable(varIndex: number) {
    this.offset = this.buf.writeUInt8(0x19, this.offset) // aload
    this.offset = this.buf.writeUInt8(varIndex, this.offset)
  }
  astore(varIndex: number) {
    this.offset = this.buf.writeUInt8(0x3a, this.offset) // astore
    this.offset = this.buf.writeUInt8(varIndex, this.offset)
  }
  invokestatic(cls: string, method: string, description: string) {
    this.offset = this.buf.writeUInt8(0xB8, this.offset) // invokestatic
    this.offset = this.buf.writeUInt16BE(this.p.getMethodRef(
      cls, method, description
    ), this.offset)
  }
  invokevirtual(cls: string, method: string, description: string) {
    this.offset = this.buf.writeUInt8(0xB6, this.offset) // invokevirtual
    this.offset = this.buf.writeUInt16BE(this.p.getMethodRef(
      cls, method, description
    ), this.offset)
  }
  swap() {
    this.offset = this.buf.writeUInt8(0x5F, this.offset) // swap
  }
  callPrint() {
    this.invokestatic('Main', 'print', '(Ljava/lang/String;)V')
  }
  newObj(cls: string) {
    this.offset = this.buf.writeUInt8(0xBB, this.offset)
    this.offset = this.buf.writeUInt16BE(this.p.addClass(
      this.p.addString(cls)
    ), this.offset)
  }
  pop() {
    this.offset = this.buf.writeUInt8(0x57, this.offset) // pop
  }
  end() {
    this.offset = this.buf.writeUInt8(0xB1, this.offset) // return
  }
  addi() {
    this.offset = this.buf.writeUInt8(0x60, this.offset) // iadd
  }
  getBuf() {
    return this.buf.slice(0, this.offset)
  }
}

enum StackType {
  Number,
  String,
  Void,
}
export function compile(source: string) {
  type Variable = ({
    type: StackType.String
  } | {
    type: StackType.Number
  }) & {
    name: string
  }
  const sourceFile = createSourceFile('main.ts', source, ScriptTarget.ES2020)
  const cls = new ClassInfo()
  const asm = new Assembler(Buffer.alloc(8192), cls)
  const p = cls.pool
  const vars: Variable[] = []
  const varIndexByName = (name: string) => vars.findIndex(i => i.name === name)
  const pushExpression = (expression: Expression): StackType => {
    const kind = expression.kind
    if (kind === SyntaxKind.Identifier) {
      const e = expression as Identifier
      const idx = varIndexByName(e.escapedText as string)
      asm.pushVariable(idx)
      return vars[idx].type
    } else if (kind === SyntaxKind.StringLiteral) {
      const e = expression as StringLiteral
      asm.pushConstant(p.addStringObj(p.addString(e.text)))
      return StackType.String
    } else if (kind === SyntaxKind.NumericLiteral) {
      const e = expression as NumericLiteral
      asm.pushConstant(p.addStringObj(p.addNumber(parseFloat(e.text))))
      return StackType.Number
    } else if (kind === SyntaxKind.BinaryExpression) {
      const e = expression as BinaryExpression
      const lt = pushExpression(e.left)
      const rt = pushExpression(e.right)
      const op = e.operatorToken
      if (op.kind === SyntaxKind.EqualsToken) {
        equal(e.left.kind, SyntaxKind.Identifier)
        const varIdx = varIndexByName((e.left as Identifier).escapedText as string)
        asm.astore(varIdx)
        return StackType.Void
      } else if (op.kind === SyntaxKind.PlusToken) {
        if (lt === rt) {
          if (lt === StackType.Number) {
            asm.addi()
            return StackType.Number
          } else if (lt === StackType.String) {
            asm.invokevirtual('java/lang/String', 'concat', '(Ljava/lang/String;)Ljava/lang/String;')
            return StackType.String
          }
        } else {
          throw new Error('Wrong type to add')
        }
      } else {
        throw new Error(`Operator not supported: ${SyntaxKind[op.kind]}`)
      }
      throw new Error('Impossible')
    } else if (kind === SyntaxKind.CallExpression) {
      const c = expression as CallExpression
      equal(c.expression.kind, SyntaxKind.Identifier)
      const func = (c.expression as Identifier).escapedText
      const args = c.arguments
      if (func !== 'print') {
        throw new TypeError(`Only print is allowed to be called`)
      }
      if (args.length !== 1) {
        throw new TypeError(`print only accept a string`)
      }
      const arg = args[0]
      const type = pushExpression(arg)
      if (type !== StackType.String) {
        throw new TypeError(`print only accept a string`)
      }
      asm.callPrint()
      return StackType.Void
    } else {
      throw new TypeError(`Unsupported kind: ${SyntaxKind[kind]}(${kind})`)
    }
  }

  for (const i of sourceFile.statements) {
    if (i.kind === SyntaxKind.VariableStatement) {
      const s = i as VariableStatement
      equal(s.declarationList.kind, SyntaxKind.VariableDeclarationList)
      for (const decl of s.declarationList.declarations) {
        equal(decl.kind, SyntaxKind.VariableDeclaration)
        equal(decl.name.kind, SyntaxKind.Identifier)
        const name = (decl.name as Identifier).escapedText as string
        if (!decl.initializer) {
          throw new TypeError(`Must have initializer`)
        }
        const value = pushExpression(decl.initializer)

        asm.astore(vars.length)
        vars.push({
          name,
          type: value as (StackType.Number | StackType.String),
        })
      }
    } else if (i.kind === SyntaxKind.ExpressionStatement) {
      const e = (i as ExpressionStatement).expression
      const t = pushExpression(e)
      if (t !== StackType.Void) {
        asm.pop()
      }
    } else {
      throw new TypeError(`Unsupported kind: ${SyntaxKind[i.kind]}(${i.kind})`)
    }
  }
  asm.end()
  cls.main = asm.getBuf()

  return cls
}
