import * as sqlite from "sqlite3";
import * as path from "path";

const db = new sqlite.Database(path.resolve("./queue.sqlite"));

const run = <T>(sql: string, params: unknown[]) => {
    return new Promise<T[]>((resolve, reject) => {
        db.all(sql, ...params, (err: unknown, rows: T[]) => {
            if (err) {
                return reject(err);
            }

            resolve(rows);
        });
    });
}

run(`
    CREATE TABLE IF NOT EXISTS queue (
        id SERIAL PRIMARY KEY,
        url TEXT NOT NULL,
        ip TEXT NOT NULL
    );
`, []);

export const enqueue = async (url: string, ip: string) => {
    const [{ count }] = await run<{ count: number }>(`
        SELECT count(*) as count
        FROM queue
        WHERE ip = ?;
    `, [ip]);

    if (count > 3) {
        return false;
    }

    await run(`
        INSERT INTO queue (url, ip)
        VALUES (?, ?);
    `, [url, ip]);

    const [{ count: queueLength }] = await run<{ count: number }>(`
        SELECT count(*) as count
        FROM queue;
    `, [])

    return queueLength;
}

export const dequeue = async () => {
    const request = await run<{ url: string, ip: string }>(`
        SELECT url, ip
        FROM queue
        ORDER BY id ASC
        LIMIT 1;
    `, []);

    if (request.length === 0) {
        return undefined;
    }

    const [{ url, ip }] = request;

    // Delete based off of url and ip in case there are duplicates
    await run(`
        DELETE FROM queue
        WHERE url = ? AND ip = ?;
    `, [url, ip]);

    return url;
}