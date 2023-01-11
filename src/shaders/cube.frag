// OpenGL Version
#version 330 core

in vec3 out_color;
out vec4 frag_color;

void main() {
    //frag_color = vec4(0.5, 0.0, 0.5, 1.0);
    frag_color = vec4(out_color, 1.0);
}