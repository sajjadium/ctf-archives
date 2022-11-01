import { addDocumentation } from ".";
import { addChild, AST, ASTStatementOrExpression, registerNode } from "./AST";

@registerNode("program")
@addChild("body", ASTStatementOrExpression, { many: true })
@addDocumentation({
  description: "Represent a program.",
  example: `<x-prog>
  <x-write>
    <x-str>Hello world!</x-str>
  </x-write>
</x-prog>`,
})
export class ASTProg extends AST<{ body: ASTStatementOrExpression[] }> {
  constructor() {
    super();
    this.classList.add("block");
    const run = document.createElement("button");
    run.innerText = "▶";
    run.classList.add("run-btn");
    run.addEventListener("click", () => this.run());
    this.append(run);
  }
  compile() {
    const { body } = this.parse();
    return body.map((n) => n.compile() + ";").join("\n");
  }

  run() {
    try {
      const body = this.compile();
      if (/[^\x00-\x7e]/.test(body)) {
        throw new Error('Ascii only, pretty please.');
      }
      const prefix = `
const write = (s) => alert(s);
const read = (s) => prompt(s);
`;
      const source = [prefix, body].join("\n");
      console.log(source);
      return eval(source);
    } catch (e) {
      alert(`${e}`);
      throw e;
    }
  }
}
