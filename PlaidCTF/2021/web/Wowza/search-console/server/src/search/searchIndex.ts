import { processSite } from "./scrape";
import { computePageRank } from "./pageRank";
import { List, Map } from "immutable";

export interface Page {
    id: number,
    name: string,
    path: string,
    rank: number;
    description: string;
};

export const buildIndex = async (domain: string, paths: string[]) => {
    const pages = await processSite(domain, paths);
    const pageRank = computePageRank(pages);

    return pageRank
        .toKeyedSeq()
        .toArray()
        .map(([path, rank], id) => {
            const { name, tokens, description } = pages.get(path) ?? { name: "unreachable", path: "unreachable", hash: "unreachable", linkPaths: ["unreachable"], tokens: ["unreachable"], description: "unreachable" };

            return {
                id,
                name,
                tokens,
                path,
                rank,
                description,
            };
        })
        .reduce(
            ([index, pageMap], page) => {
                const savedPage: Page = {
                    id: page.id,
                    name: page.name,
                    path: page.path,
                    rank: page.rank,
                    description: page.description,
                };

                const newIndex = page.tokens.reduce(
                    (idx, token) => idx.update(token, List(), (l) => l.push(page.id)),
                    index
                )
                const newPageMap = pageMap.set(page.id, savedPage);

                return [newIndex, newPageMap] as const;
            },
            [Map<string, List<number>>(), Map<number, Page>()] as const,
        );
}