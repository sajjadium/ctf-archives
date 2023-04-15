import { DocumentNode,parse, print } from "graphql/language";
import { isNode } from "graphql/language/ast";

const cache = new Map<string, DocumentNode>();

export function gql(literals: TemplateStringsArray, ...args: any[]) {
	const parts = [literals[0]];

	for (let i = 0; i < args.length; i++) {
		const arg: unknown = args[i];

		if (isNode(arg)) {
			parts.push(print(arg));
		} else if (arg === undefined || arg === null) {
			parts.push("null");
		} else {
			parts.push(JSON.stringify(arg));
		}

		parts.push(literals[i + 1]);
	}

	const source = parts.join("");

	if (cache.has(source)) {
		return cache.get(source)!;
	}

	const document = parse(source);
	cache.set(source, document);
	return document;
}
