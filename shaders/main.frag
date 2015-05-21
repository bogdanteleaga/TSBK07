#version 330

in vec2 texCoord;
in vec3 normal;
in vec3 pos;

uniform sampler2D tex;
uniform vec3 eye;
uniform float ka;
uniform float kd;
uniform float ks;
uniform float shininess;

out vec4 outColor;

void main(void)
{
    vec3 lightSource = vec3(0.0, 0.0, 0.0);
    vec3 lightColor = vec3(1.0, 1.0, 1.0);

    vec3 n = normalize(normal);
    vec3 vertexToEye = normalize(eye - pos);
    vec4 light = vec4(0, 0, 0, 0);

    // Ambient
    vec4 ambient = vec4(lightColor, 1.0) * ka;

    vec3 lightDirection = normalize(lightSource - pos);

    // Diffuse
    vec4 diffuse = vec4(0, 0, 0, 0);

    float diffuseFactor = dot(n, lightDirection);

    if (diffuseFactor > 0)
        diffuse = vec4(lightColor, 0.0) * kd * diffuseFactor;

    // Specular
    vec4 specular = vec4(0, 0, 0, 0);

    //Phong
    //vec3 reflected = normalize(reflect(lightDirection, n));
    //float specularFactor = dot(reflected, vertexToEye);
    //Blinn-Phong
    vec3 halfway = normalize(vertexToEye + lightDirection);
    float specularFactor = dot(halfway, n);
    if (specularFactor > 0)
        specular = vec4(lightColor, 0.0) * ks * pow(specularFactor, shininess);

    light = (ambient + diffuse + specular);

    //float dist = length(pos - lightSource);
    //light = light / (0.0002 * dist + 0.0007 * dist * dist);


  	outColor = texture(tex, texCoord) * light;
}
