#version 330

in  vec3 inPos;
out vec3 pos;

uniform mat4 mvpMatrix;

void main(void)
{
	gl_Position = mvpMatrix * vec4(inPos, 1.0);
    pos = inPos;
}
