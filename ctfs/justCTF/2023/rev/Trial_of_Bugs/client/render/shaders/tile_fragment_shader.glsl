precision highp float;

varying vec2 v_texCoord;
uniform sampler2D u_sampler;
uniform vec2 u_tileCount;
uniform vec2 u_tileSize;
uniform sampler2D u_mapDataSampler;

void main(void) {
  vec2 tileSamplePos = floor(v_texCoord) / u_tileCount;
  vec4 tileInfo = floor(texture2D(u_mapDataSampler, tileSamplePos) * 256.0);
  vec2 samplePos = fract(v_texCoord);
  samplePos.x = clamp(samplePos.x, 0.5 / u_tileSize.x, 1.0 - 0.5 / u_tileSize.x);
  samplePos.y = clamp(samplePos.y, 0.5 / u_tileSize.y, 1.0 - 0.5 / u_tileSize.y);
  samplePos += vec2(tileInfo.x, tileInfo.y);
  samplePos /= u_tileCount;
  gl_FragColor = texture2D(u_sampler, samplePos);
}
