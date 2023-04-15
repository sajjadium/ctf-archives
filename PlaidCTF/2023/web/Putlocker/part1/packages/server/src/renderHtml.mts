import { micromark } from "micromark";

export function renderHtml(content: string): string {
	return micromark(content);
}
