export function classes(...args: (string | undefined)[]): string {
	return args.filter((cls) => cls !== undefined).join(" ");
}
