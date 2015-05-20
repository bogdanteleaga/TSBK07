#version 330

in vec3 inPos;
in vec3 inNormal;
in vec2 inTex;
out vec2 texCoord;
out vec3 normal;
out vec3 pos;

uniform mat4 mvpMatrix;
uniform mat4 mMatrix;

void main(void)
{
  normal = mat3(mMatrix) * inNormal;
  pos = vec3(mMatrix * vec4(inPos, 1.0));

  gl_Position = mvpMatrix * vec4(inPos, 1.0);

  texCoord = inTex;
}
