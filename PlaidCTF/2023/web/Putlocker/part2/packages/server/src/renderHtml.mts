import { micromark } from "micromark";

export interface HtmlString {
	__html: string;
}

export function renderHtml(content: string): HtmlString {
	return {
		__html: micromark(content),
	};
}
