import {jest} from '@jest/globals';

let callback;
const addEventListener = jest.fn();

global.document = {
	addEventListener: jest.fn().mockImplementation((_event, cb) => {
		callback = cb;
	}),
	querySelectorAll: jest.fn().mockReturnValue([{
		addEventListener,
		previousSibling: {
			previousSibling: {
				textContent: 'textContent',
			},
		},
	}]),
};

global.navigator = {
	clipboard: {
		writeText: jest.fn(),
	},
};

await import('./image.mjs');

describe('image.mjs', () => {
	afterEach(() => {
		jest.clearAllMocks();
	});

	it('should call document.querySelectorAll', () => {
		callback();
		expect(document.querySelectorAll).toHaveBeenCalledTimes(1);
		const button = document.querySelectorAll.mock.results[0].value[0];
		expect(button.addEventListener).toHaveBeenCalledTimes(1);
	});

	it('should call navigator.clipboard.writeText', () => {
		let onClick;
		addEventListener.mockImplementationOnce((_event, cb) => {
			onClick = cb;
		});

		callback();
		expect(document.querySelectorAll).toHaveBeenCalledTimes(1);
		const button = document.querySelectorAll.mock.results[0].value[0];
		expect(addEventListener).toHaveBeenCalledTimes(1);

		onClick();
		expect(navigator.clipboard.writeText).toHaveBeenCalledTimes(1);
		expect(button.innerHTML).toBe('Copied textContent');
	});
});