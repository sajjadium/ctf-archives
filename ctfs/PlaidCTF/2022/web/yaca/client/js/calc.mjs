import astToJs from "/js/ast-to-js.mjs";
import evalCode from "/js/eval-code.mjs";
import lex from "/js/lex.mjs";
import parse from "/js/parse.mjs";

const $ = document.querySelector.bind(document);
const nameEl = $("#name");
const errorEl = $("#error");
const reportEl = $("#report");

const astProgram = $("#program");
const program = JSON.parse(astProgram.textContent);

nameEl.innerText = `Running: ${program.name}`;

reportEl.addEventListener("click", () => {
    const file = location.pathname.split("/").slice(-1)[0];
    reportEl.disabled = true;
    reportEl.innerText = "Reported!";
    fetch(`/report`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ file })
    });
})

try {
    let ast;
    if (astProgram.type === "application/x-yaca-code") {
        const tokens = lex(program.code);
        ast = parse(tokens);
    } else {
        ast = JSON.parse(program.code);
    }

    const jsProgram = astToJs(ast);
    evalCode(jsProgram);
} catch(e) {
    console.error(e);
    const msg = e instanceof Error ? e.message : "Something went wrong";
    errorEl.innerText = msg;
}
