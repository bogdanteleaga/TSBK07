#version 330

layout (location = 0) in vec3 inPos;
layout (location = 1) in vec3 inNormal;
layout (location = 2) in vec2 inTex;
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
