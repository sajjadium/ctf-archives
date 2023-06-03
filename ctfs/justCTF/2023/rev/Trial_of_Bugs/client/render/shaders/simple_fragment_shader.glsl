varying highp vec2 v_texCoord;
uniform sampler2D u_sampler;
uniform mediump vec4 u_colorMul;

void main(void) {
  gl_FragColor = texture2D(u_sampler, v_texCoord) * u_colorMul;
}
