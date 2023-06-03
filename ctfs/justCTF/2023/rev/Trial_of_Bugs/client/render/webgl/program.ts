import {ProgramDescription} from "./program_loader";
import {Texture} from "./texture";
import {mat4, vec2, vec4} from "gl-matrix";
import {StaticBuffer} from "./buffer";

export class Program<Attributes extends ReadonlyArray<string>, Uniforms extends ReadonlyArray<string>> {
    gl: WebGLRenderingContext;
    description: ProgramDescription<Attributes, Uniforms>;

    constructor(gl: WebGLRenderingContext, description: ProgramDescription<Attributes, Uniforms>) {
        this.gl = gl;
        this.description = description;
    }

    bind(values: {
        [key in (Attributes extends ReadonlyArray<infer U> ? U : never)]: StaticBuffer
    } & {
        [key in (Uniforms extends ReadonlyArray<infer U> ? U : never)]: Texture | mat4 | vec2 | vec4
    }) {
        const gl = this.gl;
        if ((gl as any)._program)
            (gl as any)._program.unbind();
        (gl as any)._program = this;

        gl.useProgram(this.description.program);
        let textureIndex = 0;
        for (const k in values) {
            if (!values.hasOwnProperty(k))
                continue;
            const value = (values as any)[k];
            if (this.description.attributes.hasOwnProperty(k)) {
                const index = (this.description.attributes as any)[k] as GLint;
                if (value instanceof StaticBuffer) {
                    gl.bindBuffer(gl.ARRAY_BUFFER, value.handle);
                    gl.vertexAttribPointer(index, value.size, value.type, value.normalized, value.stride, value.offset);
                    gl.enableVertexAttribArray(index);
                } else {
                    throw new Error(`Invalid value type passed for attribute ${k} for program ${this.description.name}`);
                }
            } else if (this.description.uniforms.hasOwnProperty(k)) {
                const index = (this.description.uniforms as any)[k] as GLint;
                if (Array.isArray(value) || value instanceof Float32Array) {
                    if (value.length === 4 * 4) {
                        gl.uniformMatrix4fv(index, false, value);
                    } else if (value.length === 4) {
                        gl.uniform4fv(index, value);
                    } else if (value.length === 2) {
                        gl.uniform2fv(index, value);
                    } else {
                        throw new Error(`Unsupported array length for uniform ${k} for program ${this.description.name}`);
                    }
                } else if (value instanceof Texture) {
                    gl.activeTexture(gl.TEXTURE0 + textureIndex);
                    gl.bindTexture(gl.TEXTURE_2D, value.handle);
                    gl.uniform1i(index, textureIndex);
                    ++textureIndex;
                } else {
                    throw new Error(`Invalid value type passed for uniform ${k} for program ${this.description.name}`);
                }
            } else {
                throw new Error(`Trying to bind invalid key: ${k} for program ${this.description.name}`);
            }
        }
    }

    unbind() {
        for (const attrib of Object.values(this.description.attributes)) {
            this.gl.disableVertexAttribArray(attrib as GLint);
        }
    }
}
