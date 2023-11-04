export const getBestImage = (files, devicePixelRatio) => {
	const clonedFiles = files.slice();
	clonedFiles.sort((a, b) => b.zoom - a.zoom);
	const file = clonedFiles.find((file) => file.zoom <= devicePixelRatio);
	return file ?? files[0];
};

globalThis.getBestImage = getBestImage;