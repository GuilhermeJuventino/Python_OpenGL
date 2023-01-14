// OpenGL version and profile being used
#version 330 core

// grabbing the output color from the vertex shader
//in vec3 out_color;
in vec2 out_texcoord_0;

out vec4 fragColor;

uniform sampler2D uv_0;

void main() {
    fragColor = texture(uv_0, out_texcoord_0);
}