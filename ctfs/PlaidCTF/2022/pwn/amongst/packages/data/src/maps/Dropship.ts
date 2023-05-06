import { Color, LevelMap } from "@amongst/game-common";

export const Dropship: LevelMap.AsJson = {
	id: "dropship",
	walls: [
		{
			start: [6, -4.5],
			end: [30, -4.5]
		},
		{
			start: [30, -4.5],
			end: [30, 13.5]
		},
		{
			start: [30, 13.5],
			end: [6, 13.5]
		},
		{
			start: [6, 13.5],
			end: [6, -4.5]
		},
		{
			start: [6, 0],
			end: [15, -4.5]
		},
		{
			start: [21, -4.5],
			end: [30, 0]
		},
	],
	devices: [
		{
			id: "computer",
			hitArea: [
				[16.5, 3],
				[19.5, 3],
				[19.5, 6],
				[16.5, 6],
			]
		},
		{
			id: "button",
			hitArea: [
				[15, -4.5],
				[20.5, -4.5],
				[20.5, -3],
				[15, -3],
			],
			graphics: {
				type: "start-panel",
				location: [18, -7]
			}
		}
	],
	spawnPoints: {
		[Color.Red]: [7.5, 0],
		[Color.Blue]: [28.5, 0],
		[Color.Green]: [9, -0.75],
		[Color.Pink]: [27, -0.75],
		[Color.Orange]: [10.5, -1.5],
		[Color.Yellow]: [25.5, -1.5],
		[Color.Black]: [12, -2.25],
		[Color.White]: [24, -2.25],
		[Color.Purple]: [13.5, -3],
		[Color.Brown]: [22.5, -3],
		[Color.Cyan]: [15, -3.75],
		[Color.Lime]: [21, -3.75],
	},
	graphics: {
		id: "dropship",
		origin: [0, 450],
		scale: 2,
		visibility: 1000
	},
	bounds: [
		[0, -18],
		[36, 30]
	]
};
