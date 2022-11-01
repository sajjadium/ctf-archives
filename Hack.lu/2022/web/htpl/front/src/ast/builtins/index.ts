import { addChild, addDocumentation, registerNode } from "../AST";
import { ASTExpression } from "../expressions";

@registerNode("write")
@addChild("value", ASTExpression)
@addDocumentation({
  description: "Represent a write expression.",
  example: `<x-write>
  <x-str>foo</x-str>
</x-write>`,
})
export class ASTWrite extends ASTExpression<{ value: ASTExpression }> {
  constructor(){
    super();
    this.classList.add("block");
  }
  compile() {
    const { value } = this.parse();
    return `write(${value.compile()})`;
  }
}

@registerNode("read")
@addChild("message", ASTExpression, { optional: true })
@addDocumentation({
  description: "Represent a read statement.",
  example: `<x-read>
  <x-identifier>foo</x-identifier>
</x-read>`,
})
export class ASTRead extends ASTExpression<{ message: ASTExpression | null }> {
  constructor(){
    super();
    this.classList.add("block");
  }
  compile() {
    const { message } = this.parse();
    return `read(${message ? message.compile() : ""})`;
  }
}
