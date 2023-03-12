#include <cstddef>
#include <string>
#include <vector>
#include <array>

#include "fpng.h"

#include "EGL/egl.h"
#include "GLES3/gl31.h"
#include "EGL/eglext.h"
// #include "EGL/eglext_angle.h"

namespace renderer {

// A lot of stuff copied from https://stackoverflow.com/questions/71396552/offscreen-rendering-with-opengl-es-3-and-egl-framebuffer-object-or-egl-pixel-bu

constexpr size_t kImageWidth { 1024 };
constexpr size_t kImageHeight { 768 };

namespace {
void assertOpenGLError(const std::string& msg) {
	GLenum error = glGetError();
	if (error != GL_NO_ERROR) {
		printf("OpenGL error for %s: 0x%x\n", msg.c_str(), error);
		exit(1);
	}
}

void assertEGLError(const std::string& msg) {
	EGLint error = eglGetError();
	if (error != EGL_SUCCESS) {
		printf("EGL error for %s: 0x%x\n", msg.c_str(), error);
		exit(1);
	}
}

#define assertTrue(cond) \
	do { \
		if (!(cond)) { \
			printf("'%s' failed\n", #cond); \
			exit(1); \
		} \
	} while (0)

EGLDisplay display;
EGLConfig config;
EGLContext context;
EGLSurface surface;
EGLint num_config;
}

void initEGL() {
	constexpr EGLint displayAttrib[] {
		EGL_RENDERABLE_TYPE, EGL_OPENGL_ES3_BIT,
		EGL_BLUE_SIZE, 8, EGL_GREEN_SIZE, 8, EGL_RED_SIZE, 8,
		EGL_SURFACE_TYPE, EGL_PBUFFER_BIT,
		EGL_NONE
	};
	constexpr EGLint contextAttrib[] {
		EGL_CONTEXT_MAJOR_VERSION, 3,
		EGL_CONTEXT_MINOR_VERSION, 1,
		EGL_CONTEXT_WEBGL_COMPATIBILITY_ANGLE, EGL_TRUE,
		EGL_CONTEXT_OPENGL_ROBUST_ACCESS_EXT, EGL_TRUE,
		EGL_NONE
	};

	constexpr EGLAttrib platformAttrib[] {
		EGL_PLATFORM_ANGLE_TYPE_ANGLE, EGL_PLATFORM_ANGLE_TYPE_VULKAN_ANGLE,
		EGL_PLATFORM_ANGLE_MAX_VERSION_MAJOR_ANGLE, -1, EGL_PLATFORM_ANGLE_MAX_VERSION_MINOR_ANGLE, -1,
		EGL_PLATFORM_ANGLE_DEVICE_TYPE_ANGLE, EGL_PLATFORM_ANGLE_DEVICE_TYPE_SWIFTSHADER_ANGLE,
		EGL_PLATFORM_ANGLE_DEBUG_LAYERS_ENABLED_ANGLE, EGL_TRUE,
		EGL_NONE
	};

	display = eglGetPlatformDisplay(EGL_PLATFORM_ANGLE_ANGLE, NULL, &platformAttrib[0]);
	assertEGLError("eglGetPlatformDisplay");

	eglInitialize(display, nullptr, nullptr);
	assertEGLError("eglInitialize");

	eglChooseConfig(display, displayAttrib, &config, 1, &num_config);
	assertEGLError("eglChooseConfig");

	context = eglCreateContext(display, config, EGL_NO_CONTEXT, contextAttrib);
	assertEGLError("eglCreateContext");

	constexpr EGLint surfaceAttrib[] = {
		EGL_WIDTH, kImageWidth,
		EGL_HEIGHT, kImageHeight,
		EGL_NONE
	};

	surface = eglCreatePbufferSurface(display, config, surfaceAttrib);
	assertEGLError("eglCreatePbufferSurface");

	eglMakeCurrent(display, surface, surface, context);
}

void initGL() {
	// Sanity check that we're using ANGLE.
	const std::string glVersion { reinterpret_cast<const char *>(glGetString(GL_VERSION)) };
	printf("GL version: %s\n", glVersion.c_str());
	assertTrue(glVersion.find("ANGLE") != std::string::npos);
}

GLuint createComputeProgram(const std::vector<char> &computeShader) {
	GLuint computeProgram { glCreateProgram() };
	const char *source[1] { computeShader.data() };
	GLuint shader = glCreateShader(GL_COMPUTE_SHADER);
	glShaderSource(shader, 1, source, nullptr);
	glCompileShader(shader);
	assertOpenGLError("Compute");
	GLint compileResult {};
	glGetShaderiv(shader, GL_COMPILE_STATUS, &compileResult);
	if (compileResult == 0) {
		GLint infoLogLength;
		glGetShaderiv(shader, GL_INFO_LOG_LENGTH, &infoLogLength);
		if (infoLogLength > 1) {
			std::vector<GLchar> infoLog(infoLogLength);
			glGetShaderInfoLog(shader, static_cast<GLsizei>(infoLog.size()), nullptr, infoLog.data());
			fprintf(stderr, "shader compilation failed: %s\n", infoLog.data());
			exit(1);
		} else {
			fprintf(stderr, "shader compilation failed with unknown reason\n");
			exit(1);
		}
	}
	glAttachShader(computeProgram, shader);
	glLinkProgram(computeProgram);
	assertTrue(glGetError() == GL_NO_ERROR);

	GLint linkStatus;
	glGetProgramiv(computeProgram, GL_LINK_STATUS, &linkStatus);
	assertTrue(linkStatus != 0);

	glDeleteShader(shader);

	return computeProgram;
}

// Used for output.
GLuint displayImage {};
GLuint fbo {};
void createSurfaceAndScratchMemory() {
	// Create texture.
	glGenTextures(1, &displayImage);
	glBindTexture(GL_TEXTURE_2D, displayImage);
	glTexStorage2D(GL_TEXTURE_2D, 1, GL_RGBA8, kImageWidth, kImageHeight);
	glBindTexture(GL_TEXTURE_2D, 0);
	assertOpenGLError("Texture creation");

	glGenFramebuffers(1, &fbo);
	glBindFramebuffer(GL_READ_FRAMEBUFFER, fbo);
	glFramebufferTexture2D(GL_READ_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, displayImage, 0);
	assertOpenGLError("FBO creation");
	assertTrue(glCheckFramebufferStatus(GL_READ_FRAMEBUFFER) == GL_FRAMEBUFFER_COMPLETE);
}

void printImage() {
	printf("Collecting image...\n");
	const size_t numChannels { 4 };
	std::vector<uint8_t> imageData;
	imageData.resize(renderer::kImageWidth * renderer::kImageWidth * numChannels);
	glReadPixels(0, 0, kImageWidth, kImageHeight, GL_RGBA, GL_UNSIGNED_BYTE, imageData.data());

	// I think there should be no bugs in this library, but hey surprise me!
	std::vector<uint8_t> output;
	fpng::fpng_encode_image_to_memory(imageData.data(), kImageWidth, kImageHeight, numChannels, output, 0);

	// Copied from https://gist.github.com/tomykaira/f0fd86b6c73063283afe550bc5d77594
	// I think there should be no bugs in this code, surprise me.
	constexpr char sEncodingTable[] = {
		'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
		'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
		'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
		'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
		'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
		'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
		'w', 'x', 'y', 'z', '0', '1', '2', '3',
		'4', '5', '6', '7', '8', '9', '+', '/'
	};
	size_t in_len = output.size();
	size_t out_len = 4 * ((in_len + 2) / 3);
	std::vector<char> ret;
	ret.resize(out_len, '\0');
	size_t i;
	char *p = ret.data();
	for (i = 0; i < in_len - 2; i += 3) {
		*p++ = sEncodingTable[(output[i] >> 2) & 0x3F];
		*p++ = sEncodingTable[((output[i] & 0x3) << 4) | ((int) (output[i + 1] & 0xF0) >> 4)];
		*p++ = sEncodingTable[((output[i + 1] & 0xF) << 2) | ((int) (output[i + 2] & 0xC0) >> 6)];
		*p++ = sEncodingTable[output[i + 2] & 0x3F];
	}
	if (i < in_len) {
		*p++ = sEncodingTable[(output[i] >> 2) & 0x3F];
		if (i == (in_len - 1)) {
			*p++ = sEncodingTable[((output[i] & 0x3) << 4)];
			*p++ = '=';
		} else {
			*p++ = sEncodingTable[((output[i] & 0x3) << 4) | ((int) (output[i + 1] & 0xF0) >> 4)];
			*p++ = sEncodingTable[((output[i + 1] & 0xF) << 2)];
		}
		*p++ = '=';
	}

	printf("Sending PNG image as base64...\n");
	printf("%s\n", ret.data());
}

}

