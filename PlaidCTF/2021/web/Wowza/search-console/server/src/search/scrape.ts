import * as crypto from "crypto";

import fetch from "node-fetch";
import { decode as decodeEntities } from "html-entities";
import { List, Map, Set } from "immutable";

import { parseDescription, parseLinks, parseTitle, parseTokens } from "./parser";

interface Page {
    hash: string;
    path: string;
    name: string;
    tokens: string[];
    description: string;
}

interface ScrapeResult extends Page {
    rawLinkPaths: string[];
}

interface DeduplicatedResult extends Page {
    linkHashes: string[];
}

export interface Result extends Page {
    linkPaths: Set<string>;
}

const scrapeOne = async (domain: string, path: string): Promise<ScrapeResult> => {
    const relativePathRegex = /^\/([^\/:]|$)/;
    if (!relativePathRegex.exec(decodeEntities(path))) {
        throw new Error(`Invalid path: ${path}`);
    }

    const url = `http://${domain}${decodeEntities(path)}`;
    const content = await fetch(url, { redirect: "error" });
    const html = await content.text();

    const hash = crypto
        .createHash("sha1")
        .update(html)
        .digest("hex");

    const tokens = parseTokens(html);
    const name = parseTitle(html) ?? path;
    const rawLinkPaths = parseLinks(html);
    const description = parseDescription(html);

    return {
        hash,
        path,
        rawLinkPaths,
        name,
        description,
        tokens,
    };
}

const traverseSite = async (domain: string, paths: string[]) => {
    const traverseOne = async (
        path: string,
        parsedPaths: Map<string, string> = Map(),
        pages: Map<string, DeduplicatedResult> = Map(),
    ): Promise<readonly [
        parsedPaths: Map<string, string>,
        pages: Map<string, DeduplicatedResult>,
        result: string | undefined,
    ]> => {
        if (parsedPaths.has(path)) {
            const hash = parsedPaths.get(path)!;
            return [parsedPaths, pages, hash];
        }

        try {
            const result = await scrapeOne(domain, path);
            if (pages.has(result.hash)) {
                return [parsedPaths.set(path, result.hash), pages, result.hash];
            }

            parsedPaths = parsedPaths.set(path, result.hash);

            const [newParsedPaths, newPages, dependencies] = await traverseMany(result.rawLinkPaths, parsedPaths, pages);
            const dedupedResult: DeduplicatedResult = {
                hash: result.hash,
                path: result.path,
                name: result.name,
                tokens: result.tokens,
                description: result.description,
                linkHashes: dependencies
                    .filter((h): h is string => h !== undefined)
                    .toSet()
                    .toArray(),
            }

            return [
                newParsedPaths,
                newPages.set(dedupedResult.hash, dedupedResult),
                dedupedResult.hash,
            ];
        } catch (e) {
            return [parsedPaths, pages, undefined]
        }
    }

    const traverseMany = async (
        paths: string[],
        parsedPaths: Map<string, string> = Map(),
        pages: Map<string, DeduplicatedResult> = Map(),
    ): Promise<readonly [
        parsedPaths: Map<string, string>,
        pages: Map<string, DeduplicatedResult>,
        results: List<string | undefined>,
    ]> => {
        return paths.reduce(
            async (acc, path) => {
                const [parsedPaths, pages, results] = await acc;
                const [newParsedPaths, newPages, result] = await traverseOne(path, parsedPaths, pages);
                return [
                    newParsedPaths,
                    newPages,
                    results.push(result)
                ] as const;
            },
            Promise.resolve([parsedPaths, pages, List<string | undefined>()] as const),
        );
    }

    const [_parsedPaths, pages, _results] = await traverseMany(paths);
    return pages;
}

export const processSite = async (domain: string, paths: string[]): Promise<Map<string, Result>> =>
    (await traverseSite(domain, paths))
        .map(({ hash, path, name, tokens, linkHashes, description }, _hash, pages): Result => {
            return {
                hash,
                tokens,
                description,
                name: name.length > 50 ? name.slice(0, 47) + "..." : name,
                path: decodeEntities(path),
                linkPaths: List(linkHashes)
                    .map((hash) => decodeEntities(pages.get(hash)!.path))
                    .toSet(),
            };
        })
        .mapKeys((_hash, result) => result.path);
