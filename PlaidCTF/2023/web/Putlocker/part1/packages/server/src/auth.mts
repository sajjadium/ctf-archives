import { Context } from "./context.mjs";
import { loadUser } from "./db.mjs";

export function assertLoggedIn(context: Context): asserts context is { user: string } {
	if (context.user === undefined) {
		throw new Error("Not logged in");
	}
}

export async function assertAdmin(context: Context & { user: string }) {
	const user = await loadUser(context.user);

	if (user.name !== "admin") {
		throw new Error("Not authorized");
	}
}
