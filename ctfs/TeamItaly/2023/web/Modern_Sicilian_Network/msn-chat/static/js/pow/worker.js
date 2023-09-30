importScripts('/static/js/pow/PoW.js');
const wasm = wasm_bindgen('/static/js/pow/PoW_bg.wasm');

addEventListener(
	'message',
	async (e) => {
		await wasm;

		const solution = await wasm_bindgen.solve(e.data.target, e.data.complexity);

		postMessage({
			solution
		});
	},
	false
);
