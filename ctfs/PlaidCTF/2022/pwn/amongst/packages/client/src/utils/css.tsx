export const classes = (...cls: (string | undefined)[]) => cls.filter((c) => c !== undefined).join(" ");
export const clsIf = (condition: boolean, cls: string) => condition ? cls : undefined;
