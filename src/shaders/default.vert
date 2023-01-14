// OpenGL version and profile being used
#version 330 core

// grabbing the input position and color from the vertex array from Python
layout (location = 0) in vec2 in_texcoord_0;
layout (location = 1) in vec3 in_normal;
layout (location = 2) in vec3 in_position;
//layout (location = 1) in vec3 in_color;

// grabbing the model, view and projection matricies from Python
uniform mat4 m_view;
uniform mat4 m_proj;
uniform mat4 m_model;

// output color value that gets shipped to the fragment shader
//out vec3 out_color;
out vec2 out_texcoord_0;

void main() {
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
    //out_color = in_color; // goes to the fragment shader
    out_texcoord_0 = in_texcoord_0;
}