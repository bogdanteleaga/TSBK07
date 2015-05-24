#version 330

in vec3 inPos;
in vec3 inNormal;
in vec2 inTex;
layout (location = 3) in mat4 instanceMatrix;
out vec2 texCoord;
out vec3 normal;
out vec3 pos;

uniform mat4 vpMatrix;

void main(void)
{
  normal = mat3(instanceMatrix) * inNormal;
  pos = vec3(instanceMatrix * vec4(inPos, 1.0));

  gl_Position = vpMatrix * instanceMatrix * vec4(inPos, 1.0);

  texCoord = inTex;
}