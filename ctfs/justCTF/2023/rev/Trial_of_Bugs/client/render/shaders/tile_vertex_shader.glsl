precision highp float;

attribute vec4 a_position;
attribute vec2 a_texCoord;
uniform mat4 u_projMatrix;
varying vec2 v_texCoord;

void main(void) {
  gl_Position = u_projMatrix * a_position;
  v_texCoord = a_texCoord;
}
