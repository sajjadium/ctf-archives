import { M, Marshaller } from "@zensors/sheriff";

export enum Color {
	Red = "Red",
	Blue = "Blue",
	Green = "Green",
	Pink = "Pink",
	Orange = "Orange",
	Yellow = "Yellow",
	Black = "Black",
	White = "White",
	Purple = "Purple",
	Brown = "Brown",
	Cyan = "Cyan",
	Lime = "Lime",
}

export namespace Color {
	export const List: Color[] = [
		Color.Red,
		Color.Blue,
		Color.Green,
		Color.Pink,
		Color.Orange,
		Color.Yellow,
		Color.Black,
		Color.White,
		Color.Purple,
		Color.Brown,
		Color.Cyan,
		Color.Lime,
	];

	export const Marshaller: Marshaller<Color> = M.union(
		M.union(
			M.lit(Color.Red),
			M.lit(Color.Blue),
			M.lit(Color.Green),
			M.lit(Color.Pink),
			M.lit(Color.Orange),
			M.lit(Color.Yellow),
		),
		M.union(
			M.lit(Color.Black),
			M.lit(Color.White),
			M.lit(Color.Purple),
			M.lit(Color.Brown),
			M.lit(Color.Cyan),
			M.lit(Color.Lime),
		),
	);
}
