import * as sqlite from "sqlite3";
import { Awaitable } from "../utils";

export const db = new sqlite.Database("./db.sqlite");

export const query = <T>(constants: TemplateStringsArray, ...args: unknown[]) => {
    return new Promise<T[]>((resolve, reject) => {
        const preparedQuery = constants.join(" ? ");
        db.all(preparedQuery, ...args, (err: any, rows: T[]) => {
            if (err) {
                reject(err);
            }

            resolve(rows);
        });
    });
};

export const queryOne = async <T>(constants: TemplateStringsArray, ...args: unknown[]) => {
    const result = await query<T>(constants, ...args);
    if (result.length !== 1) {
        throw new Error(`Expected 1, got ${result.length}`);
    }
    return result[0];
};

export const transaction = async <T>(callback: () => Awaitable<T>) => {
    try {
        await query`begin;`;
        const result = await callback();
        await query`commit;`;
        return result;
    } catch (e) {
        await query`rollback;`;
        throw e;
    }
}