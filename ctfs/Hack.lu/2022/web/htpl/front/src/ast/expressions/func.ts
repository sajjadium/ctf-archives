import { ASTExpression } from "./expression";
import {
  addChild,
  addDocumentation,
  AST,
  ASTStatementOrExpression,
  registerNode,
} from "../AST";
import { ASTIdentifier } from "./literals";

@registerNode("parameters")
@addChild("params", ASTIdentifier, { many: true })
@addDocumentation({
  description: "Represent a function parameter list.",
  example: `<x-parameters>
  <x-identifier>foo</x-identifier>
  <x-identifier>bar</x-identifier>
</x-parameters>`,
})
export class ASTParameters extends AST<{ params: ASTIdentifier[] }> {
  constructor() {
    super();
    this.classList.add("block");
  }
  compile() {
    const { params } = this.parse();
    return `${params.map((n) => n.compile()).join(", ")}`;
  }
}

@registerNode("func")
@addChild("params", ASTParameters, { optional: true })
@addChild("body", ASTStatementOrExpression, { many: true })
@addDocumentation({
  description: "Represent a function declaration.",
  example: `<x-function>
  <x-parameters>
   <x-identifier>x</x-identifier>
   <x-identifier>y</x-identifier>
  </x-parameters>
  <x-assign>
    <x-identifier>z</x-identifier>
    <x-add>
      <x-dentifier>x</x-identifier>
      <x-dentifier>y</x-identifier>
    </x-add>
  </x-assign>
  <x-return>
    <x-identifier>z</x-identifier>
  </x-return>
</x-function>`,
})
export class ASTFunction extends ASTExpression<{
  params: ASTParameters | null;
  body: ASTStatementOrExpression[];
}> {
  constructor() {
    super();
    this.classList.add("block");
  }
  compile() {
    const { params, body } = this.parse();
    return `(${params ? params.compile() : ""}) => {\n${body
      .map((s) => s.compile() + ";")
      .join("\n")}\n}`;
  }
}

@registerNode("call")
@addChild("func", ASTExpression)
@addChild("args", ASTExpression, { many: true })
@addDocumentation({
  description: "Represent a function call.",
  example: `<x-call>
  <x-identifier>myFunc</x-identifier>
  <x-str>foo</x-str>
  <x-str>bar</x-str>
</x-call>`,
})
export class ASTCall extends ASTExpression<{
  func: ASTExpression;
  args: ASTExpression[];
}> {
  constructor() {
    super();
    this.classList.add("block");
  }
  compile() {
    const { func, args } = this.parse();
    return `(${func.compile()})(${args.map((n) => n.compile()).join(", ")})`;
  }
}
