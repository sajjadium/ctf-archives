import { Map, List } from "immutable";
import { string } from "mathjs";
import { v4 as uuid } from "uuid";

import { Page, buildIndex } from "../search/searchIndex";
import { assertAllSettled, SafeError } from "../utils";
import { query, queryOne, transaction } from "./database";
import { UserAuth } from "./user";

query`
    CREATE TABLE IF NOT EXISTS site (
        domain text PRIMARY KEY,
        pages blob NOT NULL,
        indices blob NOT NULL
    );
`;

query`
    CREATE TABLE IF NOT EXISTS pending_site (
        domain text PRIMARY KEY,
        username text NOT NULL,
        validation_code text NOT NULL
    );
`;

query`
    CREATE TABLE IF NOT EXISTS user_site_ownership (
        username text NOT NULL REFERENCES user_auth (username),
        domain text NOT NULL REFERENCES site (domain),
        PRIMARY KEY (username, domain)
    );
`;

export type Index = [query: string, pageId: number[]];

export interface Site {
    domain: string;
    pages: Buffer;
    indices: Buffer;
}

export interface PendingSite {
    domain: string;
    username: string;
    validation_code: string;
}

export const getSiteIndex = async (domain: string) => {
    const results = await queryOne<Site>`
        SELECT site.* FROM site
        WHERE site.domain = ${ domain };
    `;

    const pageAsJson: Page[] = JSON.parse(results.pages.toString());
    const indexAsJson: Index[] = JSON.parse(results.indices.toString());
    const pageMap = pageAsJson
        .reduce(
            (map, page) => map.set(page.id, page),
            Map<number, Page>()
         );
    const indexMap = indexAsJson
        .reduce(
            (map, [query, pages]) =>
                map.set(
                    query,
                    pages
                        .reduce((list, page) => list.push(pageMap.get(page)!), List<Page>())
                        .sort(({ rank: r1 }, { rank: r2 }) => r2 - r1),
                ),
            Map<string, List<Page>>()
        );

    return indexMap;
}

export const getSite = async (domain: string) => {
    const result = await query<Site>`
        SELECT * FROM site
        WHERE site.domain = ${domain}
    `
    return result[0] as Site | undefined;
}

export const getSiteForUser = async (username: string, domain: string) => {
    const result = await queryOne<Site>`
        SELECT s.*
        FROM site s
        INNER JOIN user_site_ownership uso
            ON s.domain = uso.domain
        WHERE s.username = ${username}
            AND s.domain = ${domain}
    `;

    return result;
}

export const getSitesForUser = async (username: string) => {
    const siteResult = await query<Site>`
        SELECT s.*
        FROM site s
        INNER JOIN user_site_ownership uso
            ON s.domain = uso.domain
        WHERE uso.username = ${username}
    `;

    const pendingSiteResult = await query<PendingSite>`
        SELECT ps.*
        FROM pending_site ps
        WHERE ps.username = ${username}
    `;

    type Response = { domain: string, pending: false } | { domain: string, pending: true, validationCode: string };
    return siteResult
        .map<Response>(({ domain }) => ({ domain, pending: false }))
        .concat(
            pendingSiteResult
                .map(({ domain, validation_code }) => ({ domain, pending: true, validationCode: validation_code }))
        );
}

export const getSiteOwners = async (domain: string) => {
    const ownerResults = await query<UserAuth>`
        SELECT ua.* FROM site s
        INNER JOIN user_site_ownership uso
            ON uso.domain = s.domain
        INNER JOIN user_auth ua
            ON ua.username = uso.username
        WHERE s.domain = ${domain};
    `;

    const owners = ownerResults.map(({ username }) => username);
    return { owners };
}

export const getPendingSitesForOwner = async (username: string) => {
    const pendingSites = await query<PendingSite>`
        SELECT * FROM pending_site
        WHERE username = ${username}
    `;
    return pendingSites;
}

export const registerSite = async (username: string, domain: string) => {
    const site = await getSite(domain);
    if (site) {
        throw new SafeError(401, "Site already exists");
    }

    const validationCode = uuid();
    await query`
        INSERT INTO pending_site (domain, validation_code, username)
        VALUES (${domain}, ${validationCode}, ${username});
    `;

    return validationCode;
}

export const validateSite = async (username: string, domain: string, validation_code: string) => {
    await transaction(async () => {
        const pendingSitePromise = query<PendingSite>`
                SELECT * FROM pending_site
                WHERE domain = ${domain}
                    AND username = ${username}
                    AND validation_code = ${validation_code};`
            .then((validationResults) => {
                if (validationResults.length !== 1) {
                    throw new SafeError(401, "Invalid validation code");
                };
            })
            .then(() => query`
                DELETE FROM pending_site
                WHERE domain = ${domain};
            `);

        const siteInsertPromise = query`
            INSERT INTO site (domain, pages, indices)
            VALUES (${domain}, ${JSON.stringify([])}, ${JSON.stringify([])});
        `;

        const ownershipInsertPromise = query`
            INSERT INTO user_site_ownership (username, domain)
            VALUES (${username}, ${domain});
        `;

        const results = await Promise.allSettled([pendingSitePromise, siteInsertPromise, ownershipInsertPromise]);
        assertAllSettled(results);
    })
}

export const scrapeSite = async (domain: string) => {
    const [index, pageMap] = await buildIndex(domain, ["/"]);
    const pageArray: Page[] = pageMap.valueSeq().toArray();
    const indexArray: Index[] = index
        .map((l) => l.toArray())
        .entrySeq()
        .toArray();

    await query`
        UPDATE site
        SET pages = ${JSON.stringify(pageArray)}, indices = ${JSON.stringify(indexArray)}
        WHERE domain = ${domain};
    `;
}