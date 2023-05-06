import { parse, stringify } from "qs";
import { useLocation } from "react-router";

export function useQs(): Record<string, unknown> {
	const location = useLocation();
	return parse(location.search, {
		ignoreQueryPrefix: true,
		decoder: (str) => {
			str = decodeURIComponent(str);

			if (!Number.isNaN(Number(str))) {
				return Number(str);
			} else if (str === "✓") {
				return true;
			} else if (str === "✗") {
				return false;
			} else {
				return str;
			}
		}
	});
}

export function encodeQs(qs: Record<string, unknown>) {
	return stringify(qs, {
		encoder: (x) => {
			if (typeof x === "boolean") {
				return x ? "✓" : "✗";
			} else if (typeof x === "number") {
				return x.toString();
			} else {
				// eslint-disable-next-line @typescript-eslint/no-unsafe-return
				return x;
			}
		}
	});
}
