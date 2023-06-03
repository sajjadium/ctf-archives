export type ImageArrayDescription = {
    data: Uint8Array,
    width: number,
    height: number,
    format: GLenum,
    internalFormat?: GLenum
}

export class Texture {
    gl: WebGLRenderingContext;
    handle: WebGLTexture;

    constructor(gl: WebGLRenderingContext, image: HTMLImageElement | ImageArrayDescription, filtering: GLenum = gl.LINEAR) {
        this.gl = gl;
        this.handle = gl.createTexture()!;
        gl.bindTexture(gl.TEXTURE_2D, this.handle);
        if (image instanceof Image) {
            gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, image);
        } else {
            const internalFormat = image.internalFormat !== undefined ? image.internalFormat : image.format;
            gl.texImage2D(gl.TEXTURE_2D, 0, internalFormat, image.width, image.height, 0, image.format, gl.UNSIGNED_BYTE, image.data);
        }
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, filtering);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, filtering);
    }

    destroy() {
        this.gl.deleteTexture(this.handle);
    }
}
