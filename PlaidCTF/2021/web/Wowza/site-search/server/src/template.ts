import * as path from "path";

import * as fs from "fs-extra";
import { Result } from "./client";

const formatResult = (domain: string) => (result: Result) => {
    return `
<div class="result">
    <a class="link" href="${new URL(result.path, "http://" + domain)}" target="__blank">${result.name}</a>
    <div class="description">
        ${result.description}
    </div>
</div>
    `;
};

export const formatTemplate = async (domain: string, results: Result[]) => {
    const template = await
        fs.readFile(path.join(__dirname, "../../client/index.html"))
            .then((val) => val.toString());

    return template.replace(
        "<!-- SEARCH RESULTS -->",
        results.map(formatResult(domain)).join(""),
    );
};