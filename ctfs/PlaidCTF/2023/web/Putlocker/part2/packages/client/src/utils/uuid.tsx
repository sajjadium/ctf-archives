const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

export function uuidify(id?: string): string {
	if (id !== undefined && uuidRegex.test(id)) {
		return id;
	} else {
		// A lot of server code gets mad if we send it an invalid uuid, so we'll just send it a valid one
		return "00000000-0000-0000-0000-000000000000";
	}
}
