#version 150

in  vec3 inPos;

void main(void)
{
	gl_Position = vec4(inPos, 1.0);
}
