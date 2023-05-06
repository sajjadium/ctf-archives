import { ASTChildren, registerMetaNode } from "..";
import { addChild, addDocumentation, registerNode } from "../AST";
import { ASTExpression, ASTIdentifier } from "../expressions";
import { ASTStatement } from "./statement";

@registerMetaNode("assignment")
@addDocumentation({
  description: "Assigns a value to a variable",
})
export class ASTAssignment<T extends ASTChildren> extends ASTStatement<T> {}

@registerNode("const")
@addChild("identifier", ASTIdentifier)
@addChild("value", ASTExpression)
@addDocumentation({
  description: "Represent a constant declaration.",
  example: `<x-const>
  <x-identifier>foo</x-identifier>
  <x-str>bar</x-str>
</x-const>`,
})
export class ASTConst extends ASTAssignment<{
  identifier: ASTIdentifier;
  value: ASTExpression;
}> {
  constructor() {
    super();
    this.classList.add("block");
  }
  compile() {
    const { identifier, value } = this.parse();

    return `const ${identifier.compile()}=${value.compile()}`;
  }
}

@registerNode("let")
@addChild("identifier", ASTIdentifier)
@addChild("value", ASTExpression)
@addDocumentation({
  description: "Represent a variable declaration.",
  example: `<x-let>
  <x-identifier>foo</x-identifier>
  <x-str>bar</x-str>
</x-let>`,
})
export class ASTLet extends ASTAssignment<{
  identifier: ASTIdentifier;
  value: ASTExpression;
}> {
  constructor() {
    super();
    this.classList.add("block");
  }
  compile() {
    const { identifier, value } = this.parse();

    return `let ${identifier.compile()}=${value.compile()}`;
  }
}
