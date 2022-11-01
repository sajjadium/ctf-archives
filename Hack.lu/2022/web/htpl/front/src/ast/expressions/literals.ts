import { registerMetaNode } from "..";
import { addDocumentation, registerNode } from "../AST";
import { ASTExpression } from "./expression";

@registerMetaNode("literal")
@addDocumentation({
  description: "Represent a literal value.",
})
export class ASTLiteral extends ASTExpression {
  _unique = Symbol();
  constructor(type: string, color: string) {
    super();
    this.dataset.type = type;
    this.style.setProperty("--color", color);
  }
}

@registerNode("str")
@addDocumentation({
  description: "Represent a string literal.",
  example: `<x-str>foo</x-str>`,
})
export class ASTStr extends ASTLiteral {
  constructor() {
    super("string", "#ff7043");
  }

  compile() {
    return JSON.stringify(this.textContent ?? "");
  }
}

@registerNode("num")
@addDocumentation({
  description: "Represent a number literal.",
  example: `<x-num>42</x-num>`,
})
export class ASTNum extends ASTLiteral {
  constructor() {
    super("number", "#26c6da");
  }
  compile() {
    return Number(this.textContent || 0).toString();
  }
}

@registerNode("true")
@addDocumentation({
  description: "Represent a true literal.",
  example: `<x-true></x-true>`,
})
export class ASTTrue extends ASTLiteral {
  constructor() {
    super("boolean", "#66bb6a");
    this.dataset.value = "true";
  }
  compile() {
    return "true";
  }
}

@registerNode("false")
@addDocumentation({
  description: "Represent a false literal.",
  example: `<x-false></x-false>`,
})
export class ASTFalse extends ASTLiteral {
  constructor() {
    super("boolean", "#66bb6a");
    this.dataset.value = "false";
  }
  compile() {
    return "false";
  }
}

@registerNode("null")
@addDocumentation({
  description: "Represent a null literal.",
  example: `<x-null></x-null>`,
})
export class ASTNull extends ASTLiteral {
  constructor() {
    super("null", "#9575cd");
    this.dataset.value = "<NULL>";
  }
  compile() {
    return "null";
  }
}

@registerNode("identifier")
@addDocumentation({
  description: "Represent an identifier.",
  example: `<x-identifier>foo</x-identifier>`,
})
export class ASTIdentifier extends ASTLiteral {
  constructor() {
    super("identifier", "#ffa726");
  }

  compile() {
    const name = this.textContent ?? "";
    if (!name.match(/^[_a-z0-9]+$/i)) {
      throw new SyntaxError(`Invalid identifier`);
    }
    return `$${name}$`;
  }
}
