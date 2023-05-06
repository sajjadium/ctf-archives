import * as math from "mathjs";
import { Map, List, Set } from "immutable";
import { Result } from "./scrape";

const exp = (m: math.Matrix, e: number) =>
    List(Array(e)).reduce((agg) => math.multiply(agg, m) as math.Matrix, math.identity(m.size()[0]) as math.Matrix);

export const computePageRank = (pages: Map<string, Result>) => {
    const allPages = pages.reduce((map, page) => map.set(page.path, Set()), Map<string, Set<string>>())
    const backLinks =
        pages.reduce(
            (bl, page) =>
                page.linkPaths.reduce(
                    (blInner, link) => blInner.update(link, (p = Set()) => p.add(page.path)),
                    bl,
                ),
            allPages,
        );

    const keys = backLinks.keySeq().toArray();
    if (keys.length === 0) {
        return Map<string, number>();
    }

    const matrix = math.matrix(Array.from(new Array(keys.length), (_, i) =>
        Array.from(new Array(keys.length), (_, j) => {
            const to = keys[i];
            const from = keys[j];

            if (to === from) return 0;
            const links = backLinks.get(from);
            const denominator = links?.size ?? 0;

            if (denominator === 0) {
                return 1 / keys.length;
            }

            if (links?.has(to)) {
                return 1 / denominator;
            }

            return 0;
        })
    ));

    const dim = keys.length;

    const equilibrium = math.multiply<math.Matrix>(
        exp(matrix, 10),
        math.divide(math.ones([dim, 1]), dim)
    );

    return keys.reduce(
        (agg, key, i) => agg.set(key, equilibrium.get([i, 0]) as number),
        Map<string, number>()
    );
}