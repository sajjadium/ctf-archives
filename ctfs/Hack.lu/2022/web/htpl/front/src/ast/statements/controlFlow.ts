import { ASTStatement } from "./statement";
import {
  addChild,
  addDocumentation,
  ASTStatementOrExpression,
  registerNode,
} from "../AST";
import { ASTExpression } from "../expressions";

@registerNode("if")
@addChild("condition", ASTExpression)
@addChild("then", ASTStatementOrExpression, { many: true })
@addDocumentation({
  description: "Represent an if statement.",
  example: `<x-if>
  <x-identifier>foo</x-identifier>
  <x-return>
    <x-identifier>foo</x-identifier>
  </x-return>
</x-if>`,
})
export class ASTIf extends ASTStatement<{
  condition: ASTExpression;
  then: ASTStatementOrExpression[];
}> {
  constructor() {
    super();
    this.classList.add("block");
  }
  compile() {
    const { condition, then } = this.parse();

    return `if(${condition.compile()}){\n${then
      .map((s) => s.compile() + ";")
      .join("\n")}\n}`;
  }
}

@registerNode("while")
@addChild("condition", ASTExpression)
@addChild("body", ASTStatementOrExpression, { many: true })
@addDocumentation({
  description: "Represent a while statement.",
  example: `<x-while>
  <x-identifier>foo</x-identifier>
  <x-dec>
    <x-identifier>foo</x-identifier>
  </x-dec>
</x-while>`,
})
export class ASTWhile extends ASTStatement<{
  condition: ASTExpression;
  body: ASTStatementOrExpression[];
}> {
  constructor() {
    super();
    this.classList.add("block");
  }
  compile() {
    const { condition, body } = this.parse();

    return `while(${condition.compile()}){\n${body
      .map((s) => s.compile() + ";")
      .join("\n")}\n}`;
  }
}

@registerNode("return")
@addChild("value", ASTExpression, { optional: true })
@addDocumentation({
  description: "Represent a return statement.",
  example: `<x-return>
  <x-identifier>foo</x-identifier>
</x-return>`,
})
export class ASTReturn extends ASTStatement<{
  value: ASTExpression | null;
}> {
  constructor() {
    super();
    this.classList.add("block");
  }
  compile() {
    const { value } = this.parse();
    return `return ${value ? `${value.compile()}` : ""}`;
  }
}

@registerNode("continue")
@addDocumentation({
  description: "Represent a continue statement.",
  example: `<x-continue></x-continue>`,
})
export class ASTContinue extends ASTStatement {
  compile() {
    return "continue";
  }
}

@registerNode("break")
@addDocumentation({
  description: "Represent a break statement.",
  example: `<x-break></x-break>`,
})
export class ASTBreak extends ASTStatement {
  compile() {
    return "break";
  }
}
