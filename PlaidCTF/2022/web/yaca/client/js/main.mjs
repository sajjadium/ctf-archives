const $ = document.querySelector.bind(document);
const nameEl = $("#name");
const uploadEl = $("#upload");
const programEl = $("#program");
const contentTypeEl = $("#content-type");

uploadEl.addEventListener("click", async () => {
    const code = programEl.value;
    // We use logical or instead of nullish coalescing because
    // [input] values are always coerced to a string
    const name = nameEl.value || nameEl.getAttribute("placeholder");
    const type = contentTypeEl.value;

    const res = await fetch("/upload", {
        method: "POST",
        headers: {
            "content-type": "application/json",
        },
        body: JSON.stringify({ type, program: { name, code } })
    });

    const url = await res.text();
    window.location.href = url;
});

const staticAst = `{
    "kind": "binop",
    "op": "divide",
    "values": [
        {
            "kind": "binop",
            "op": "add",
            "values": [
                {
                    "kind": "unop",
                    "op": "negate",
                    "value": { "kind": "variable", "variable": "b"}
                },
                {
                    "kind": "function",
                    "name": "sqrt",
                    "argument": {
                        "kind": "binop",
                        "op": "subtract",
                        "values": [
                            {
                                "kind": "binop",
                                "op": "exponent",
                                "values": [
                                    { "kind": "variable", "variable": "b"},
                                    { "kind": "number", "value": 2}
                                ]
                            },
                            {
                                "kind": "binop",
                                "op": "multiply",
                                "values": [
                                    { "kind": "number", "value": 4 },
                                    {
                                        "kind": "binop",
                                        "op": "multiply",
                                        "values": [
                                            { "kind": "variable", "variable": "a" },
                                            { "kind": "variable", "variable": "c" }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                }
            ]
        },
        {
            "kind": "binop",
            "op": "multiply",
            "values": [
                { "kind": "number", "value": 2 },
                { "kind": "variable", "variable": "a" }
            ]
        }
    ]
}`;

const staticCode = `(-b + sqrt(b^2 - 4a*c)) / 2a`;

const resetTextArea = () => {
    const contentType = contentTypeEl.value;

    if (contentType === "application/x-yaca-ast") {
        programEl.value = staticAst;
    } else {
        programEl.value = staticCode;
    }
}

contentTypeEl.addEventListener("change", resetTextArea);
resetTextArea();
