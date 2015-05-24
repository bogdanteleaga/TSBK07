#version 330

in vec3 pos;
out vec4 out_Color;

void main(void)
{
	out_Color = vec4(pos, 1.0);

}
