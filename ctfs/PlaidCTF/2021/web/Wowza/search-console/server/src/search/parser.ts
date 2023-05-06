import { decode as decodeEntities } from "html-entities";
import { List } from "immutable";

export const parseLinks = (html: string) => {
    const anchorRegex = /<\s*a\s*[^>]*href\s*=\s*"([^\s"]+)"\s*.*>/g;

    const links: string[] = [];
    let match: RegExpExecArray | null = null;
    while (match = anchorRegex.exec(html)) {
        const path = match[1];
        links.push(path);
    }

    return links;
}

const getBody = (html: string) => {
    const components = html.split(/<\s*body[^>]*>/g);
    const body = components.length >= 2 ? components[1] : html;
    return body
        .replace(/<[^>]*>/g, " ")
        .split(/\s+/g)
}

export const parseDescription = (html: string) => {
    const body = getBody(html);
    return body
        .slice(0, 50)
        .join(" ")
        .trim();
}

export const parseTokens = (html: string) => {
    return List(getBody(html))
        .map((x) => x.toLowerCase().replace(/[^a-z0-9]+/, ""))
        .filter((x) => x !== "")
        .toSet()
        .toArray();
}

export const parseTitle = (html: string) => {
    const titleRegex = /<\s*title[^>]*>([^<]+)<\/\s*title\s*>/;
    return titleRegex.exec(html)?.[1].trim();
}