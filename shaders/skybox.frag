#version 330

in vec3 texCoord;

uniform samplerCube tex;

out vec4 outColor;

void main(void)
{
  	outColor = texture(tex, texCoord);
}
