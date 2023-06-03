attribute vec4 a_position;
attribute vec2 a_texCoord;
attribute vec4 a_color;
uniform mat4 u_projMatrix;
varying highp vec2 v_texCoord;
varying mediump vec4 v_color;

void main(void) {
  gl_Position = u_projMatrix * a_position;
  v_texCoord = a_texCoord;
  v_color = a_color;
}
