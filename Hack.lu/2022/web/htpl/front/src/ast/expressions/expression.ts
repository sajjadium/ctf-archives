import { addDocumentation, registerMetaNode } from "..";
import { ASTChildren, ASTStatementOrExpression } from "../AST";

@registerMetaNode("expression")
@addDocumentation({
  description: "Represent an expression.",
})
export class ASTExpression<
  T extends ASTChildren = {}
> extends ASTStatementOrExpression<T> {}
