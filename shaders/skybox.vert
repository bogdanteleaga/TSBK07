#version 330

in vec3 inPos;
out vec3 texCoord;

uniform mat4 vMatrix;
uniform mat4 pMatrix;

void main(void)
{
  vec4 position = pMatrix * vec4(mat3(vMatrix) * inPos, 1.0);
  gl_Position = position.xyww;

  texCoord = inPos;
}
