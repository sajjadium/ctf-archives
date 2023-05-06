import { ASTExpression, ASTIdentifier } from ".";
import { registerMetaNode } from "..";
import { addChild, addDocumentation, ASTChildren, registerNode } from "../AST";

@registerMetaNode("unary-op")
@addDocumentation({
  description: "Represent an unary operator.",
})
export class ASTUnaryOp<T extends ASTChildren> extends ASTExpression<T> {
  constructor(op: string) {
    super();
    this.dataset.op = op;
  }
}

@registerMetaNode("bin-op")
@addDocumentation({
  description: "Represent a binary operator.",
})
export class ASTBinOp extends ASTExpression<{
  left: ASTExpression;
  right: ASTExpression;
}> {}

function createBinaryOp(name: string, op: string) {
  @registerNode(name)
  @addChild("left", ASTExpression)
  @addChild("right", ASTExpression)
  @addDocumentation({
    description: `Represent a ${op} operator.`,
    example: `<x-${name}>
  <x-identifier>x</x-identifier>
  <x-identifier>y</x-identifier>
</x-${name}>`,
  })
  class cls extends ASTBinOp {
    constructor() {
      super();
      this.dataset.op = op;
    }
    compile() {
      const { left, right } = this.parse();
      return `${left.compile()}${op}${right.compile()}`;
    }
  }
  return cls;
}

export const ASTAdd = createBinaryOp("add", "+");
export const ASTSub = createBinaryOp("sub", "-");
export const ASTMul = createBinaryOp("mul", "*");
export const ASTDiv = createBinaryOp("div", "/");
export const ASTMod = createBinaryOp("mod", "%");
export const ASTPow = createBinaryOp("pow", "**");
export const ASTEq = createBinaryOp("eq", "==");
export const ASTNe = createBinaryOp("ne", "!=");
export const ASTLt = createBinaryOp("lt", "<");
export const ASTGt = createBinaryOp("gt", ">");
export const ASTLe = createBinaryOp("le", "<=");
export const ASTGe = createBinaryOp("ge", ">=");
export const ASTAnd = createBinaryOp("and", "&&");
export const ASTOr = createBinaryOp("or", "||");
export const ASTXor = createBinaryOp("xor", "^");

@registerNode("dec")
@addChild("name", ASTIdentifier)
@addDocumentation({
  description: "Represent a decrement operator.",
  example: `<x-dec>
  <x-identifier>x</x-identifier>
</x-dec>`,
})
export class ASTDec extends ASTUnaryOp<{ name: ASTIdentifier }> {
  constructor() {
    super("--");
  }
  compile(): string {
    const { name } = this.parse();
    return `--${name.compile()}`;
  }
}

@registerNode("inc")
@addChild("name", ASTIdentifier)
@addDocumentation({
  description: "Represent an increment operator.",
  example: `<x-inc>
  <x-identifier>x</x-identifier>
</x-inc>`,
})
export class ASTInc extends ASTUnaryOp<{ name: ASTIdentifier }> {
  constructor() {
    super("++");
  }
  compile(): string {
    const { name } = this.parse();
    return `++${name.compile()}`;
  }
}

@registerNode("not")
@addChild("expr", ASTExpression)
@addDocumentation({
  description: "Represent a not operator.",
  example: `<x-not>
  <x-identifier>x</x-identifier>
</x-not>`,
})
export class ASTNot extends ASTUnaryOp<{ expr: ASTExpression }> {
  constructor() {
    super("!");
  }
  compile(): string {
    const { expr } = this.parse();
    return `!${expr.compile()}`;
  }
}
