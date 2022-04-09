const $ = document.querySelector.bind(document);

const prepareInputs = (variables, onChange) => {
    const inputEl = $("#input");

    for (const node of [...inputEl.childNodes]) {
        node.remove();
    }

    for (const variable of variables) {
        const input = document.createElement("input");
        input.setAttribute("type", "text");
        input.setAttribute("placeholder", `${variable.slice(4)}`);
        input.setAttribute("value", "");
        input.addEventListener("keyup", () => {
            let value = Number(input.value);
            if (isNaN(value)) {
                value = 0;
            }

            onChange(variable, value);
        });
        inputEl.appendChild(input);
    }
}

const updateOutput = (result) => {
    // Float truncation
    if (typeof result === "number" && Math.floor(result) !== result) {
        result = result.toFixed(2);
    }

    const $ = document.querySelector.bind(document);
    const outputEl = $("#output");

    outputEl.innerText = result;
}


export default ({ code, variables }) => {
    const varList = [...variables].sort((a, b) => a.localeCompare(b));
    const fn = new Function(...varList, `return (${code});`);
    const values = new Map(varList.map((val) => [val, 0]));

    const refresh = () => {
        const result = fn(...varList.map((val) => values.get(val)));

        if (isNaN(result)) {
            throw new Error("Output was not a number")
        }

        $("#error").innerText = "";
        updateOutput(result);
    }

    const onChange = (variable, value) => {
        values.set(variable, value);
        refresh();
    }

    prepareInputs(varList, onChange);

    refresh();
}