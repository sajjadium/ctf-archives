export class StaticBuffer {
    gl: WebGLRenderingContext;
    handle: WebGLBuffer;
    size: number;
    type: GLenum;
    stride: number = 0;
    normalized: boolean = false;
    private dynamicDraw: boolean = false;

    constructor(gl: WebGLRenderingContext, data: any, size: number, options?: { dynamicDraw?: boolean }) {
        this.gl = gl;
        this.handle = gl.createBuffer()!;
        this.size = size;
        this.type = 0;
        this.dynamicDraw = options?.dynamicDraw || false;
        this.update(data);
    }

    update(data: any) {
        const gl = this.gl;

        if (data instanceof Float32Array) {
            this.type = gl.FLOAT;
        } else if (data instanceof Array) {
            data = new Float32Array(data);
            this.type = gl.FLOAT;
        } else {
            throw new Error("data has unknown type");
        }

        gl.bindBuffer(gl.ARRAY_BUFFER, this.handle);
        gl.bufferData(gl.ARRAY_BUFFER, data, this.dynamicDraw ? gl.DYNAMIC_DRAW : gl.STATIC_DRAW);
    }

    get offset() {
        return 0;
    }

    destroy() {
        this.gl.deleteBuffer(this.handle);
    }

}
