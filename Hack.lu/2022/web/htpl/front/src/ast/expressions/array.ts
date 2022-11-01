import { addChild, addDocumentation, registerNode } from "../AST";
import { ASTExpression } from "./expression";

@registerNode("array")
@addChild("children", ASTExpression, { many: true })
@addDocumentation({
  description: "Represent an array literal.",
  example: `<x-array>
  <x-str>foo</x-str>
  <x-str>bar</x-str>
</x-array>`,
})
export class ASTArray extends ASTExpression<{ children: ASTExpression[] }> {
  constructor() {
    super();
    this.classList.add("block");
  }
  compile() {
    const { children } = this.parse();
    return `[${children.map((n) => n.compile()).join(", ")}]`;
  }
}

@registerNode("pop")
@addChild("array", ASTExpression)
@addDocumentation({
  description: "Represent an array pop.",
  example: `<x-pop>
  <x-identifier>myArray</x-identifier>
</x-pop>`,
})
export class ASTPop extends ASTExpression<{ array: ASTExpression }> {
  compile() {
    const { array } = this.parse();
    return `(${array.compile()}).pop()`;
  }
}

@registerNode("push")
@addChild("array", ASTExpression)
@addChild("value", ASTExpression)
@addDocumentation({
  description: "Represent an array push.",
  example: `<x-push>
  <x-identifier>myArray</x-identifier>
  <x-str>bar</x-str>
</x-push>`,
})
export class ASTPush extends ASTExpression<{
  array: ASTExpression;
  value: ASTExpression;
}> {
  compile() {
    const { array, value } = this.parse();
    return `(${array.compile()}).push(${value.compile()})`;
  }
}

@registerNode("map")
@addChild("array", ASTExpression)
@addChild("func", ASTExpression)
@addDocumentation({
  description: "Represent an array map.",
  example: `<x-map>
  <x-identifier>myArray</x-identifier>
  <x-identifier>myFunc</x-identifier>
</x-map>`,
})
export class ASTMap extends ASTExpression<{
  array: ASTExpression;
  func: ASTExpression;
}> {
  compile() {
    const { array, func } = this.parse();
    return `(${array.compile()}).map(${func.compile()})`;
  }
}
