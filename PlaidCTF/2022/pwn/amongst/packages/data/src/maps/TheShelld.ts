import { Color, LevelMap } from "@amongst/game-common";

export const TheShelld: LevelMap.AsJson = {
	id: "shelld",
	walls: [
		// Cafeteria
		{
			start: [0, 0],
			end: [25.5, 0]
		},
		{
			start: [25.5, 0],
			end: [25.5, 9]
		},
		{
			start: [25.5, 15],
			end: [25.5, 19.5]
		},
		{
			start: [25.5, 19.5],
			end: [0, 19.5]
		},
		{
			start: [0, 19.5],
			end: [0, 15]
		},
		{
			start: [0, 9],
			end: [0, 0]
		},
		{
			start: [21, 0],
			end: [25.5, 4.5]
		},
		{
			start: [19.8, 2.4],
			end: [5.7, 2.4],
			transparent: true
		},
		{
			start: [5.7, 2.4],
			end: [5.7, 6.6],
			transparent: true
		},
		{
			start: [5.7, 6.6],
			end: [19.8, 6.6],
			transparent: true
		},
		{
			start: [19.8, 6.6],
			end: [19.8, 2.4],
			transparent: true
		},
		{
			start: [19.8, 8.4],
			end: [5.7, 8.4],
			transparent: true
		},
		{
			start: [5.7, 8.4],
			end: [5.7, 12.6],
			transparent: true
		},
		{
			start: [5.7, 12.6],
			end: [19.8, 12.6],
			transparent: true
		},
		{
			start: [19.8, 12.6],
			end: [19.8, 8.4],
			transparent: true
		},
		{
			start: [19.8, 14.4],
			end: [5.7, 14.4],
			transparent: true
		},
		{
			start: [5.7, 14.4],
			end: [5.7, 18.6],
			transparent: true
		},
		{
			start: [5.7, 18.6],
			end: [19.8, 18.6],
			transparent: true
		},
		{
			start: [19.8, 18.6],
			end: [19.8, 14.4],
			transparent: true
		},
		{
			start: [0, 1.5],
			end: [4, 1.5],
			transparent: true
		},
		{
			start: [4, 1.5],
			end: [4, 0],
			transparent: true
		},

		// Cafeteria-Admin Hallway
		{
			start: [25.5, 9],
			end: [34.5, 9]
		},
		{
			start: [34.5, 15],
			end: [25.5, 15]
		},

		// Admin
		{
			start: [34.5, 9],
			end: [34.5, -3]
		},
		{
			start: [34.5, -3],
			end: [40.5, -3]
		},
		{
			start: [46.5, -3],
			end: [49.5, -3]
		},
		{
			start: [49.5, -3],
			end: [49.5, 19.5]
		},
		{
			start: [49.5, 19.5],
			end: [34.5, 19.5]
		},
		{
			start: [34.5, 19.5],
			end: [34.5, 15]
		},
		{
			start: [34.5, 0],
			end: [37.5, -3]
		},
		{
			start: [49.5, 13.5],
			end: [47.1, 13.5],
			transparent: true
		},
		{
			start: [47.1, 13.5],
			end: [47.1, 18],
			transparent: true
		},
		{
			start: [47.1, 18],
			end: [40.5, 18],
			transparent: true
		},
		{
			start: [40.5, 18],
			end: [40.5, 19.5],
			transparent: true
		},

		// Admin-Communications-Navigation Hallway
		{
			start: [40.5, -3],
			end: [40.5, -21]
		},
		{
			start: [46.5, -21],
			end: [46.5, -15]
		},
		{
			start: [46.5, -15],
			end: [57, -15]
		},
		{
			start: [57, -9],
			end: [46.5, -9]
		},
		{
			start: [46.5, -9],
			end: [46.5, -3]
		},

		// Navigation
		{
			start: [57, -15],
			end: [57, -16.5]
		},
		{
			start: [57, -16.5],
			end: [70.5, -16.5]
		},
		{
			start: [70.5, -16.5],
			end: [70.5, -1.5]
		},
		{
			start: [70.5, -1.5],
			end: [57, -1.5]
		},
		{
			start: [57, -1.5],
			end: [57, -9]
		},
		{
			start: [67.5, -16.5],
			end: [70.5, -13.5]
		},
		{
			start: [70.5, -4.5],
			end: [67.5, -1.5]
		},

		// Communications
		{
			start: [40.5, -15],
			end: [21, -15]
		},
		{
			start: [25.5, -15],
			end: [25.5, -28.5],
		},
		{
			start: [25.5, -33],
			end: [49.5, -33]
		},
		{
			start: [49.5, -33],
			end: [49.5, -21]
		},
		{
			start: [49.5, -21],
			end: [46.5, -21]
		},
		{
			start: [40.5, -21],
			end: [37.5, -21]
		},
		{
			start: [37.5, -21],
			end: [31.5, -15]
		},

		// Communications-Medbay-UpperEngine Hallway
		{
			start: [25.5, -28.5],
			end: [15, -28.5]
		},
		{
			start: [15, -28.5],
			end: [15, -24]
		},
		{
			start: [7.5, -24],
			end: [7.5, -28.5]
		},
		{
			start: [7.5, -28.5],
			end: [-4.5, -28.5],
		},
		{
			start: [-4.5, -28.5],
			end: [-4.5, -22.5]
		},
		{
			start: [-4.5, -22.5],
			end: [0, -22.5]
		},
		{
			start: [0, -18],
			end: [-10.5, -18]
		},
		{
			start: [-10.5, -12],
			end: [-10.5, -28.5]
		},
		{
			start: [-10.5, -28.5],
			end: [-22.5, -28.5]
		},
		{
			start: [-22.5, -33],
			end: [25.5, -33]
		},

		// Medbay
		{
			start: [15, -24],
			end: [21, -24]
		},
		{
			start: [21, -24],
			end: [21, 0]
		},
		{
			start: [21, -4.5],
			end: [7.5, -4.5]
		},
		{
			start: [7.5, -4.5],
			end: [7.5, -16.5]
		},
		{
			start: [7.5, -16.5],
			end: [0, -16.5]
		},
		{
			start: [0, -16.5],
			end: [0, -18]
		},
		{
			start: [0, -22.5],
			end: [0, -24]
		},
		{
			start: [0, -24],
			end: [7.5, -24]
		},
		{
			start: [17.2, -4.5],
			end: [17.2, -6.9],
			transparent: true
		},
		{
			start: [17.2, -6.9],
			end: [7.5, -6.9],
			transparent: true
		},

		// UpperEngine
		{
			start: [-22.5, -28.5],
			end: [-22.5, -15]
		},
		{
			start: [-22.5, -15],
			end: [-25.5, -15]
		},
		{
			start: [-31.5, -15],
			end: [-34.5, -15]
		},
		{
			start: [-34.5, -15],
			end: [-34.5, -33]
		},
		{
			start: [-34.5, -33],
			end: [-22.5, -33]
		},
		{
			start: [-34.5, -30],
			end: [-31.5, -33]
		},

		// UpperEngine-Electrical-LowerEngine Hallway
		{
			start: [-25.5, -15],
			end: [-25.5, -9]
		},
		{
			start: [-25.5, -9],
			end: [-19.5, -9]
		},
		{
			start: [-19.5, -3],
			end: [-25.5, -3]
		},
		{
			start: [-25.5, -3],
			end: [-25.5, 3]
		},
		{
			start: [-31.5, 3],
			end: [-31.5, -15]
		},

		// Electrical
		{
			start: [-19.5, -9],
			end: [-19.5, -12]
		},
		{
			start: [-19.5, -12],
			end: [7.5, -12]
		},
		{
			start: [4.5, -12],
			end: [4.5, -4.5]
		},
		{
			start: [4.5, -4.5],
			end: [-4.5, -4.5]
		},
		{
			start: [-4.5, -4.5],
			end: [-4.5, 9]
		},
		{
			start: [-4.5, -0],
			end: [-19.5, -0]
		},
		{
			start: [-19.5, -0],
			end: [-19.5, -3]
		},
		{
			start: [-16.5, -12],
			end: [-16.5, -3]
		},
		{
			start: [-16.5, -3],
			end: [-13.5, -3]
		},
		{
			start: [-13.5, -3],
			end: [-13.5, -12]
		},
		{
			start: [-7.5, 0],
			end: [-7.5, -9],
		},
		{
			start: [-7.5, -9],
			end: [-10.5, -9],
		},
		{
			start: [-10.5, -9],
			end: [-10.5, 0],
		},

		// LowerEngine
		{
			start: [-25.5, 3],
			end: [-22.5, 3]
		},
		{
			start: [-22.5, 3],
			end: [-22.5, 9]
		},
		{
			start: [-22.5, 15],
			end: [-22.5, 19.5]
		},
		{
			start: [-22.5, 19.5],
			end: [-34.5, 19.5]
		},
		{
			start: [-34.5, 19.5],
			end: [-34.5, 3]
		},
		{
			start: [-34.5, 3],
			end: [-31.5, 3]
		},
		{
			start: [-31.5, 19.5],
			end: [-34.5, 16.5]
		},

		// LowerEngine-Cafeteria Hallway
		{
			start: [-22.5, 9],
			end: [0, 9]
		},
		{
			start: [0, 15],
			end: [-22.5, 15]
		},

		// Secret
		{
			start: [22.5, -10.5],
			end: [33, -10.5]
		},
		{
			start: [33, -10.5],
			end: [33, -6]
		},
		{
			start: [33, -6],
			end: [22.5, -6]
		},
		{
			start: [22.5, -6],
			end: [22.5, -10.5]
		},
	],
	devices: [
		{
			id: "vending",
			hitArea: [
				[0, 0],
				[4, 0],
				[4, 4],
				[0, 4]
			],
			graphics: {
				type: "vending-machine",
				location: [2, 0]
			}
		},
		{
			id: "login",
			hitArea: [
				[43.5, 16.5],
				[49.5, 16.5],
				[49.5, 19.5],
				[43.5, 19.5]
			],
			graphics: {
				type: "monitor",
				location: [47.4, 18]
			}
		},
		{
			id: "data-upload",
			hitArea: [
				[34.5, 16.5],
				[37.5, 16.5],
				[37.5, 19.5],
				[34.5, 19.5]
			],
			graphics: {
				type: "access-point",
				location: [34.5, 18],
				layer: 1
			}
		},
		{
			id: "data-download",
			hitArea: [
				[25.5, -18],
				[28.5, -18],
				[28.5, -15],
				[25.5, -15]
			],
			graphics: {
				type: "access-point",
				location: [25.5, -16.5],
				layer: 1
			}
		},
		{
			id: "centrifuge",
			hitArea: [
				[10.5, -7.5],
				[13.5, -7.5],
				[13.5, -4.5],
				[10.5, -4.5]
			],
			graphics: {
				type: "centrifuge",
				location: [12, -5.7]
			}
		},
		{
			id: "keypad",
			hitArea: [
				[-34.5, 3],
				[-31.5, 3],
				[-31.5, 4.5],
				[-34.5, 4.5]
			],
			graphics: {
				type: "keypad",
				location: [-33, 1]
			}
		},
		{
			id: "vent-cafeteria",
			hitArea: [
				[15, 0],
				[18, 0],
				[18, 1.5],
				[15, 1.5]
			],
			graphics: {
				type: "vent",
				location: [16.5, 0.75],
				layer: -1
			}
		},
		{
			id: "vent-navigation",
			hitArea: [
				[64.5, -16.5],
				[67.5, -16.5],
				[67.5, -15],
				[64.5, -15]
			],
			graphics: {
				type: "vent",
				location: [66, -15.75],
				layer: -1
			}
		},
		{
			id: "vent-communications",
			hitArea: [
				[46.5, -33],
				[49.5, -33],
				[49.5, -31.5],
				[46.5, -31.5]
			],
			graphics: {
				type: "vent",
				location: [48, -32.25],
				layer: -1
			}
		},
		{
			id: "vent-medbay",
			hitArea: [
				[18, -6],
				[21, -6],
				[21, -4.5],
				[18, -4.5]
			],
			graphics: {
				type: "vent",
				location: [19.5, -5.25],
				layer: -1
			}
		},
		{
			id: "vent-electrical-west",
			hitArea: [
				[-13.5, -12],
				[-10.5, -12],
				[-10.5, -10.5],
				[-13.5, -10.5]
			],
			graphics: {
				type: "vent",
				location: [-12, -11.25],
				layer: -1
			}
		},
		{
			id: "vent-electrical-east",
			hitArea: [
				[1.5, -6],
				[4.5, -6],
				[4.5, -4.5],
				[1.5, -4.5]
			],
			graphics: {
				type: "vent",
				location: [3, -5.25],
				layer: -1
			}
		},
		{
			id: "vent-lower-engine",
			hitArea: [
				[-25.5, 3],
				[-22.5, 3],
				[-22.5, 4.5],
				[-25.5, 4.5]
			],
			graphics: {
				type: "vent",
				location: [-24, 3.75],
				layer: -1
			}
		},
		{
			id: "vent-hallway",
			hitArea: [
				[-10.5, -19.5],
				[-7.5, -19.5],
				[-7.5, -18],
				[-10.5, -18]
			],
			graphics: {
				type: "vent",
				location: [-9, -18.75],
				layer: -1
			}
		},
		{
			id: "conspiracy-board",
			hitArea: [
				[24, -10.5],
				[31.5, -10.5],
				[31.5, -9],
				[24, -9]
			],
			graphics: {
				type: "conspiracy-board",
				location: [27.75, -12.5],
				hideInDark: true
			}
		},
		{
			id: "emergency-button",
			hitArea: [
				[9, 7.5],
				[16.5, 7.5],
				[16.5, 13.5],
				[9, 13.5]
			],
			graphics: {
				type: "emergency-button",
				location: [12.75, 9.875]
			}
		},
		{
			id: "satellite",
			hitArea: [
				[-40.5, 36],
				[-34.5, 36],
				[-34.5, 42],
				[-40.5, 42]
			],
			graphics: {
				type: "satellite",
				location: [-37.5, 39],
				layer: -1
			}
		}
	],
	spawnPoints: {
		[Color.Red]: [11.5, 8],
		[Color.Blue]: [11.5, 13],
		[Color.Green]: [9, 8],
		[Color.Pink]: [16.5, 13],
		[Color.Orange]: [14, 8],
		[Color.Yellow]: [6.5, 13],
		[Color.Black]: [19, 13],
		[Color.White]: [16.5, 8],
		[Color.Purple]: [14, 13],
		[Color.Brown]: [9, 13],
		[Color.Cyan]: [19, 8],
		[Color.Lime]: [6.5, 8],
	},
	graphics: {
		id: "shelld",
		scale: 1,
		origin: [1012.5, 1125],
		visibility: 16
	},
	bounds: [
		[-40.5, -45],
		[79.5, 42]
	]
};
