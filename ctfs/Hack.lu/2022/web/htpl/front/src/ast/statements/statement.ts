import { addDocumentation, registerMetaNode } from "..";
import { ASTChildren, ASTStatementOrExpression } from "../AST";

@registerMetaNode("statement")
@addDocumentation({
  description: "Represent a statement.",
})
export class ASTStatement<
  T extends ASTChildren = {}
> extends ASTStatementOrExpression<T> {
  constructor() {
    super();
  }
}
