#version 330

in vec3 inPos;
out vec3 texCoord;

uniform mat4 vMatrix;
uniform mat4 pMatrix;

void main(void)
{
  gl_Position = pMatrix * vec4(mat3(vMatrix) * inPos, 1.0);

  texCoord = inPos;
}
