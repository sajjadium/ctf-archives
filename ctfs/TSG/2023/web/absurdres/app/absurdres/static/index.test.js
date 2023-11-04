import {getBestImage} from './index.mjs';

describe('getBestImage', () => {
	it('should return the best image based on current devicePixelRatio', () => {
		const files = [
			{zoom: 1},
			{zoom: 2},
			{zoom: 3},
		];

		expect(getBestImage(files, 1)).toBe(files[0]);
		expect(getBestImage(files, 1.5)).toBe(files[0]);
		expect(getBestImage(files, 2)).toBe(files[1]);
		expect(getBestImage(files, 3)).toBe(files[2]);
	});

	it('should return the first image if no image is found', () => {
		const files = [
			{zoom: 1},
			{zoom: 2},
			{zoom: 3},
		];

		expect(getBestImage(files, 0)).toBe(files[0]);
		expect(getBestImage(files, 0.5)).toBe(files[0]);
	});

	it('should not alter the original array', () => {
		const files = [
			{zoom: 1},
			{zoom: 3},
			{zoom: 2},
		];

		getBestImage(files, 1.5);
		expect(files).toEqual([
			{zoom: 1},
			{zoom: 3},
			{zoom: 2},
		]);
	});
});