#include "renderer.hpp"

#include <iostream>
#include <cstdio>
#include <cinttypes>
#include <chrono>
#include <unistd.h>
#include <fcntl.h>

#include "fpng.cpp"

int main() {
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);

	printf("You like https://www.shadertoy.com/ ?\n\n");
	printf("Then you would love HXP's 'ShaderToyPlusPlus'\n\n");

	printf("Trying to init drivers...\n");
	renderer::initEGL();
	renderer::initGL();
	printf("\n");

	printf("Creating rendering surface...\n");
	renderer::createSurfaceAndScratchMemory();
	printf("\n");

	printf("How many programs do you need?\n");
	size_t numPrograms {};
	const int r { scanf("%zu", &numPrograms) };
	if (r != 1 || numPrograms == 0 || numPrograms > 4) {
		printf("Invalid number\n");
		exit(1);
	}
	std::vector<GLuint> programs;
	for (size_t i {}; i < numPrograms; ++i) {
		std::vector<char> data;
		data.resize(4096);
		printf("Give me compute shader (max %zu):\n", data.size() - 1);

		// Read 1 byte a time
		for (size_t q {}; q < data.size() - 1; ++q) {
			const ssize_t r { read(0, &data[q], 1) };
			if (r <= 0) {
				printf("failed to read\n");
				exit(1);
			}
		}

		data[std::min(data.size() - 1, strnlen(data.data(), data.size()))] = '\x00';
		printf("Trying to create program...\n");
		GLuint program { renderer::createComputeProgram(data) };
		programs.push_back(program);
	}
	printf("\n");

	// No more input is necessary.
	int null = open("/dev/null", O_WRONLY);
	if (null < 0) {
		printf("Failed to open /dev/null");
		exit(1);
	}
	close(0);
	dup2(null, 0);

	constexpr int32_t kTimeBinding { 0 };
	constexpr int32_t kImageBinding { 8 };
	constexpr int32_t kImageBindingInput { 9 };

	printf("ShaderToyPlusPlus shader program info:\n");
	printf("- time            (seconds)     : loc %d\n", kTimeBinding);
	printf("- Output 2D image (RGBA, 8 bpp) : binding %d\n", kImageBinding);
	printf("- Input 2D image  (RGBA, 8 bpp) : binding %d\n", kImageBindingInput);
	printf("\n");

	printf("Binding resources...\n");
	glBindImageTexture(kImageBinding, renderer::displayImage, 0, GL_FALSE, 0, GL_READ_WRITE, GL_RGBA8);
	glBindImageTexture(kImageBindingInput, renderer::displayImage, 0, GL_FALSE, 0, GL_READ_WRITE, GL_RGBA8);

	printf("Start rendering...\n");
	for (size_t i {}; i < programs.size(); ++i) {
		const std::clock_t timeStart { std::clock() };
		// Bind program.
		glUseProgram(programs[i]);

		// Use for noise if you want.
		glUniform1f(kTimeBinding, float(timeStart) / CLOCKS_PER_SEC);

		// Run, wait for execution to finish and wait for accesses to become visible.
		glDispatchCompute(1, 1, 1);
		glFinish();
		glMemoryBarrier(GL_SHADER_IMAGE_ACCESS_BARRIER_BIT);

		const std::clock_t timeEnd { std::clock() };
		const float elapsedSeconds { float(timeEnd - timeStart) / CLOCKS_PER_SEC };
		renderer::printImage();
		printf("Rendering took: %f seconds\n\n", elapsedSeconds);
	}

	// WAR: Sleep a bit to get output to the other side.
	sleep(2);

	return 0;
}
