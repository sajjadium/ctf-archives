import { Color } from "@amongst/game-common";

export function getSpotColors(color: Color) {
	switch (color) {
		case Color.Red: return { primary: 0xd71e22, shadow: 0x7a0838, interior: 0x7e0c16 };
		case Color.Blue: return { primary: 0x132ed1, shadow: 0x09158e, interior: 0x050d36 };
		case Color.Green: return { primary: 0x117f2d, shadow: 0x0a4d2e, interior: 0x002209 };
		case Color.Pink: return { primary: 0xed54ba, shadow: 0xab2bad, interior: 0x471835 };
		case Color.Orange: return { primary: 0xef7d0e, shadow: 0xb33f15, interior: 0x412105 };
		case Color.Yellow: return { primary: 0xf6f658, shadow: 0xc38823, interior: 0x404118 };
		case Color.Black: return { primary: 0x3f474e, shadow: 0x1e1f26, interior: 0x111111 };
		case Color.White: return { primary: 0xd6e0f0, shadow: 0x8394bf, interior: 0x393d3c };
		case Color.Purple: return { primary: 0x6b31bc, shadow: 0x3c177c, interior: 0x151224 };
		case Color.Brown: return { primary: 0x71491e, shadow: 0x5e2615, interior: 0x110f02 };
		case Color.Cyan: return { primary: 0x38fedb, shadow: 0x24a8be, interior: 0x0e433a };
		case Color.Lime: return { primary: 0x50ef39, shadow: 0x15a742, interior: 0x0a2d0d };
	}
}
