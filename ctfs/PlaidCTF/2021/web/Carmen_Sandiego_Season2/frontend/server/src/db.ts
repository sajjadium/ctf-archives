import { Pool, PoolClient } from "pg";

export const pool = new Pool({ max: 10 });

export async function transaction<T>(fn: (client: PoolClient) => Promise<T>): Promise<T> {
	const client = await pool.connect();
	let result: T;

	try {
		await client.query("BEGIN");
		result = await fn(client);
		await client.query("COMMIT");
	} catch (err) {
		await client.query("ROLLBACK");
		throw err;
	} finally {
		client.release();
	}

	return result;
}

