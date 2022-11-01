import type { AST, ASTConstructor } from "./AST";


interface Visitor {
  hasNext(): boolean;
  hasNextOfType<T extends AST>(checker?: ASTTypeChecker<T>): boolean;
  getNext<T extends AST>(checker?: ASTTypeChecker<T>): T;
  maybeGetNext<T extends AST>(checker?: ASTTypeChecker<T>): T | null;
  getRemaining<T extends AST>(checker?: ASTTypeChecker<T>): T[];
}
type ASTTypeChecker<T extends AST> = (node: AST) => node is T;

function* iterAstChildren(
  el: Element,
  baseClass: ASTConstructor
): Generator<AST> {
  for (const child of Array.from(el.children)) {
    console.log("CHILD", child)
    if (child instanceof baseClass) {
      yield child;
    } else {
      yield* iterAstChildren(child, baseClass);
    }
  }
}

export function createVisitor(node: AST, baseClass: ASTConstructor) {
  const children = [...iterAstChildren(node, baseClass)];
  let pos = 0;

  return <Visitor>{
    hasNext() {
      return pos < children.length;
    },
    hasNextOfType(checker) {
      if (!this.hasNext()) {
        return false;
      }
      if (!checker) {
        return true;
      }
      return checker(children[pos]);
    },
    getNext(checker) {
      if (!this.hasNext()) {
        throw new SyntaxError(`Missing node for ${node.constructor.nodeName}`);
      }
      if (!this.hasNextOfType(checker)) {
        throw new SyntaxError(`Invalid node type for ${node.constructor.nodeName}`);
      }
      return children[pos++];
    },
    maybeGetNext(checker) {
      if (!this.hasNextOfType(checker)) {
        return null;
      }
      return this.getNext(checker);
    },
    getRemaining(checker) {
      const remaining = children.slice(pos);
      if (checker && !remaining.every(checker)) {
        throw new SyntaxError(`Invalid node type for ${node.constructor.nodeName}`);
      }
      pos = children.length;
      return remaining;
    },
  };
}
