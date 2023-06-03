varying highp vec2 v_texCoord;
varying mediump vec4 v_color;
uniform sampler2D u_sampler;

void main(void) {
  gl_FragColor = texture2D(u_sampler, v_texCoord) * v_color;
}
