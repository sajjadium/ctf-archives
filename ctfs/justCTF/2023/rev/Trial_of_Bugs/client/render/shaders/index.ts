import {ProgramLoader} from "../webgl/program_loader";

export function createProgramCollection(gl: WebGLRenderingContext) {
    const loader = new ProgramLoader(gl);

    return {
        simple: loader.loadProgram({
            name: 'simple',
            vertexSource: require('./simple_vertex_shader.glsl'),
            fragmentSource: require('./simple_fragment_shader.glsl'),
            attributes: ['a_position', 'a_texCoord'] as const,
            uniforms: ['u_projMatrix', 'u_sampler', 'u_colorMul'] as const
        }),
        colored: loader.loadProgram({
            name: 'colored',
            vertexSource: require('./colored_vertex_shader.glsl'),
            fragmentSource: require('./colored_fragment_shader.glsl'),
            attributes: ['a_position', 'a_texCoord', 'a_color'] as const,
            uniforms: ['u_projMatrix', 'u_sampler'] as const
        }),
        tile: loader.loadProgram({
            name: 'tile',
            vertexSource: require('./tile_vertex_shader.glsl'),
            fragmentSource: require('./tile_fragment_shader.glsl'),
            attributes: ['a_position', 'a_texCoord'] as const,
            uniforms: ['u_projMatrix', 'u_sampler', 'u_tileCount', 'u_tileSize', 'u_mapDataSampler'] as const
        })
    };
}

export type ProgramCollection = ReturnType<typeof createProgramCollection>;
