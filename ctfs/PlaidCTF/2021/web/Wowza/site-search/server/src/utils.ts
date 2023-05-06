export const getBody = (html: string) => {
    const components = html.split(/<\s*body[^>]*>/g);
    const body = components.length >= 2 ? components[1] : html;
    return body
        .replace(/<[^>]*>/g, " ")
        .split(/\s+/g)
}
