// OpenGL version and profile being used
#version 330 core

// grabbing the output color from the vertex shader
in vec3 out_color;
out vec4 fragColor;

void main() {
    fragColor = vec4(out_color, 1.0);
}