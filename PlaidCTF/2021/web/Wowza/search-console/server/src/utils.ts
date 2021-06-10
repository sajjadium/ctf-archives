import * as dns from "dns";

import { M } from "@zensors/sheriff";

export type Awaitable<T> = T | Promise<T>;

interface PromiseFulfilledResult<T> {
    status: "fulfilled";
    value: T;
}

interface PromiseRejectedResult {
    status: "rejected";
    reason: any;
}

type PromiseSettledResult<T> = PromiseFulfilledResult<T> | PromiseRejectedResult;


export class SafeError extends Error {
    public code;
    public error;

    constructor(code: number, error: string) {
        super(`[${code}]: ${error}`);
        this.code = code;
        this.error = error
    }
}

export const getTextRecords = (domain: string) => {
    return new Promise<string[]>((resolve, reject) => {
        dns.resolveTxt(domain, (err, records) => {
            resolve((records ?? []).map(([record]) => record));
        })
    })
};

export const domainIsNotLocalhost = (domain: string) => {
    return new Promise<boolean>((resolve, reject) => {
        dns.lookup(domain, (err, address) => {
            resolve(address !== "127.0.0.1")
        })
    });
}

export const MDomain = M.custom(M.str, (domain) => {
    if (!domain.match(/^[a-z0-9\.\-\_]{2,64}$/)) {
        throw new Error("Invalid domain");
    }
});

export const assertAllSettled = <T extends any[]>(results: { [K in keyof T]: PromiseSettledResult<T[K]> }): T => {
    const firstError = results.find((res): res is PromiseRejectedResult => res.status === "rejected");
    if (firstError !== undefined) {
        throw firstError.reason;
    }

    return results.map((res) => (res as PromiseFulfilledResult<unknown>).value) as T;
};