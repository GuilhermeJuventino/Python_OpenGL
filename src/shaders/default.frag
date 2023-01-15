// OpenGL version and profile being used
#version 330 core

// grabbing the output texture coordinates, normals, and fragment position from the vertex shader
//in vec3 out_color;
in vec2 out_texcoord_0;
in vec3 out_normal;
in vec3 frag_pos;

// final output colors of the model that gets rendered
out vec4 fragColor;

// a structure containing the values for the light source that comes from Python
struct Light {
    // light source's position
    vec3 position;

    // ambient lighting intensity
    vec3 Ia;

    // diffuse lighting intensity
    vec3 Id;

    // specular lighting intensity
    vec3 Is;
};

uniform sampler2D uv_0;

// creating an instance of the uniform Light struct
uniform Light light;

// current position of the camera
uniform vec3 cam_pos;

// function that gets the rbg color values of the textures and return updated color values taking lighting into account
vec3 getLight(vec3 color) {
    // the model's normals
    vec3 Normal = normalize(out_normal);

    // ambient light
    vec3 ambient = light.Ia;

    // diffuse light
    vec3 light_dir = normalize(light.position - frag_pos);
    float diff = max(0, dot(light_dir, Normal));
    vec3 diffuse = diff * light.Id;

    // specular light
    vec3 view_dir = normalize(cam_pos - frag_pos);
    vec3 reflect_dir = reflect(-light_dir, Normal);
    float spec = pow(max(dot(view_dir, reflect_dir), 0), 32);
    vec3 specular = spec * light.Is;
    
    // returning the updated color values taking lighting into account
    return color * (ambient + diffuse + specular);
}

void main() {
    // color values of the model's texture
    vec3 color = texture(uv_0, out_texcoord_0).rgb;

    // updating the color values taking lighting into account
    color = getLight(color);

    // final fragment color values of the texture that gets rendered to the screen
    fragColor = vec4(color, 1.0);
}