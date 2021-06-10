import { List, Map } from "immutable";

import { Router, marshalBody } from "@zensors/expedite";
import { M } from "@zensors/sheriff";

import { Site } from "../state";
import { MDomain } from "../utils";
import { Page } from "../search/searchIndex";

export const searchRouter = new Router()

searchRouter.post("/")
    .then(marshalBody(M.obj({ domain: MDomain, query: M.arr(M.str) })))
    .return<{ name: string, path: string }[]>(async (req) => {
        const query = req.body.query
            .map((q) => q.replace(/[^a-zA-Z0-9]+/g, ""))
            .filter((q) => q !== "");

        const index = await Site.getSiteIndex(req.body.domain);
        return List(query)
            .flatMap((q) => index.get(q) ?? List<Page>())
            .reduce(
                (agg, page) => agg.update(page.id, ([p, count] = [page, 0]) => [p, count + 1]),
                Map<number, [Page, number]>(),
            )
            .valueSeq()
            .sort(([p1, c1], [p2, c2]) => p2.rank * c2 - p1.rank * c1)
            .map(([{ name, path, description }]) => ({ name, path, description }))
            .toArray()
            .slice(0, 10);
    });