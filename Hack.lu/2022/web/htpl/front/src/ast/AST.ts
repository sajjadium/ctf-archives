import { createVisitor } from "./visitor";

export type Documentation = {
  name?: string;
  description?: string;
  example?: string;
};

export interface ChildDefinition {
  name: string;
  type: ASTConstructor;
  many: boolean;
  optional: boolean;
}

export interface AST<T extends ASTChildren = {}> extends HTMLElement {
  compile(): string;
  constructor: ASTConstructor;
}

export interface ASTConstructor<T extends ASTChildren = {}> {
  new (...args: any[]): AST<T>;
  children: ChildDefinition[] | null;
  documentation: Documentation;
  nodeName: string;
  __proto__?: ASTConstructor;
}

export type ASTChildren = Record<string, AST | AST[] | null>;

export class AST<T extends ASTChildren> extends HTMLElement {
  static nodeName = "";
  static children = null;
  static documentation: Documentation = {};

  constructor() {
    super();
    this.dataset.name = this.constructor.nodeName;
    let c: ASTConstructor = this.constructor;
    while (c != AST) {
      this.classList.add(c.nodeName);
      c = c.__proto__!;
    }
  }
  compile(): string {
    throw new Error("Method not implemented.");
  }

  parse(): T {
    const visitor = createVisitor(this, AST as ASTConstructor);
    const result: ASTChildren = {};

    try {
      for (const child of this.constructor.children ?? []) {
        const name = child.name;
        const checker = is(child.type);

        if (child.many) {
          result[name] = visitor.getRemaining(checker);
        } else if (child.optional) {
          result[name] = visitor.maybeGetNext(checker);
        } else {
          result[name] = visitor.getNext(checker);
        }
      }
    } catch (e) {
      if (e instanceof Error) {
        this.dataset.error = `${e.message}`;
      }
      throw e;
    }

    return result as T;
  }
}

export function is<T extends AST>(type: ASTConstructor) {
  return function (node: AST): node is T {
    console.log(node, "is", type);
    return node instanceof type;
  };
}

export function addChild(
  name: string,
  type: ASTConstructor,
  options: { optional?: true; many?: true } = {}
) {
  const child = {
    name,
    type,
    optional: options.optional ?? false,
    many: options.many ?? false,
  };

  return function (constructor: ASTConstructor) {
    if (!constructor.children) {
      constructor.children = [];
    }
    constructor.children.unshift(child);
  };
}

export function addDocumentation(doc: Documentation) {
  return function (constructor: ASTConstructor) {
    constructor.documentation = { ...constructor.documentation, ...doc };
  };
}

export const registeredNodes = new Set<ASTConstructor>();

export function registerNode(name: string) {
  return function (constructor: ASTConstructor) {
    constructor.nodeName = name;
    registeredNodes.add(constructor);
    customElements.define(`x-${name}`, constructor);
  };
}
export function registerMetaNode(tag: string) {
  return function (constructor: ASTConstructor) {
    constructor.nodeName = tag;
    registeredNodes.add(constructor);
  };
}

@registerMetaNode("statement-or-expression")
@addDocumentation({
  description: "Represent a statement or an expression.",
})
export class ASTStatementOrExpression<
  T extends ASTChildren = {}
> extends AST<T> {}
