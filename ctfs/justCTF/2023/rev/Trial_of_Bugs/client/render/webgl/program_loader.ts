import {Program} from "./program";

export type ProgramDescription<Attributes extends ReadonlyArray<string>, Uniforms extends ReadonlyArray<string>> = {
    name: string,
    program: WebGLProgram,
    attributes: {
        [key in (Attributes extends ReadonlyArray<infer U> ? U : never)]: GLint
    },
    uniforms: {
        [key in (Uniforms extends ReadonlyArray<infer U> ? U : never)]: WebGLUniformLocation
    }
}

export class ProgramLoader {
    gl: WebGLRenderingContext;

    constructor(gl: WebGLRenderingContext) {
        this.gl = gl;
    }

    private compileShader(programName: string, type: GLenum, typeName: string, source: string) {
        const gl = this.gl;
        const shader = gl.createShader(type);
        if (shader === null)
            throw new Error('Failed to create shader');
        gl.shaderSource(shader, source);
        gl.compileShader(shader);

        if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
            const log = gl.getShaderInfoLog(shader);
            throw new Error(`Failed to compile ${typeName} shader "${programName}": ${log}`);
        }
        return shader;
    }

    private compileProgram(programName: string, vertexSource: string, fragmentSource: string) {
        const gl = this.gl;
        const vertexShader = this.compileShader(programName, gl.VERTEX_SHADER, 'vertex', vertexSource);
        const fragmentShader = this.compileShader(programName, gl.FRAGMENT_SHADER, 'fragment', fragmentSource);

        const program = gl.createProgram();
        if (program === null)
            throw new Error('Failed to create program');
        gl.attachShader(program, vertexShader);
        gl.attachShader(program, fragmentShader);
        gl.linkProgram(program);

        if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
            const log = gl.getProgramInfoLog(program);
            throw new Error(`Failed to link program "${programName}": ${log}`);
        }
        return program;
    }

    private getAttribLocation(program: WebGLProgram, programName: string, name: string) {
        const ret = this.gl.getAttribLocation(program, name);
        if (ret === -1)
            throw new Error(`Unable to find attribute "${name}" in program "${programName}"`);
        return ret;
    }

    private getUniformLocation(program: WebGLProgram, programName: string, name: string) {
        const ret = this.gl.getUniformLocation(program, name);
        if (ret === null)
            throw new Error(`Unable to find uniform "${name}" in program "${programName}"`);
        return ret;
    }

    loadProgram<Attributes extends ReadonlyArray<string>, Uniforms extends ReadonlyArray<string>>(description: {
        name: string,
        vertexSource: string,
        fragmentSource: string,
        attributes: Attributes,
        uniforms: Uniforms
    }): Program<Attributes, Uniforms> {
        const program = this.compileProgram(description.name, description.vertexSource, description.fragmentSource);
        return new Program(this.gl, {
            name: description.name,
            program,
            attributes: Object.fromEntries(description.attributes.map(x => [x, this.getAttribLocation(program, description.name, x)])) as any,
            uniforms: Object.fromEntries(description.uniforms.map(x => [x, this.getUniformLocation(program, description.name, x)])) as any,
        });
    }
}
