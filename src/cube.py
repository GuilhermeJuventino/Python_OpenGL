import pygame
import numpy as np
import glm


class Cube:
    def __init__(self, app):
        self.app = app # app of class GraphicsEngine
        self.ctx = self.app.ctx # OpenGL context

        self.vbo = self.get_vbo() # Vertex Buffer Object
        self.shader_program = self.get_shader_program("cube")
        self.vao = self.get_vao() # Vertex Array Object
        self.m_model = self.get_model_matrix() # Model Matrix

        self.texture = self.get_texture("textures/test.png")

        self.on_init()

    def get_texture(self, path):
        texture = pygame.image.load(path).convert()
        texture = pygame.transform.flip(texture, flip_x=False, flip_y=True)
        
        texture = self.ctx.texture(size=texture.get_size(), components=3,
        data=pygame.image.tostring(texture, "RGB"))

        return texture

    def get_vertex_data(self):
        # A list of points containing xyz coordinates and rgb color values
        verticies = [
            # x   y  z     r    g    b
            (-1, -1, 1, 0.5, 0.0, 0.0, 0.0, 0.0),  # IDX 0:
            (1, -1, 1, 0.0, 0.5, 0.0, 1.0, 0.0),  # IDX 1:
            (1, 1, 1, 0.0, 0.0, 0.5, 1.0, 1.0),  # IDX 2:
            (-1, 1, 1, 0.5, 0.5, 0.5, 0.0, 1.0),   # IDX 3:

            (-1, 1, -1, 0.5, 0.0, 0.0, 1.0, 1.0), # IDX 4
            (-1, -1, -1, 0.0, 0.5, 0.0, 1.0, 0.0), # IDX 5
            (1, -1, -1, 0.0, 0.0, 0.5, 0.0, 0.0), # IDX 6
            (1, 1, -1, 0.5, 0.5, 0.5, 0.0, 1.0) # IDX 7
        ]

        # A list of triangles based on the indicies of the verticies list
        indicies = [
            (0, 2, 3), (0, 1, 2),
            (1, 7, 2), (1, 6, 7),
            (6, 5, 4), (4, 7, 6),
            (3, 4, 5), (3, 5, 0),
            (3, 7, 4), (3, 2, 7),
            (0, 6, 1), (0, 5, 6)
        ]

        data = []

        """for triangle in indicies:
            for ind in triangle:
                data.append(ind)"""
        
        # parsing the verticies and indicies arrays to generate the vertex data
        for a in indicies:
            for ind in a:
                data.append(verticies[ind])
        
        # converting the vertex data into an array with float 32 numbers that can be read by OpenGL
        vertex_data = np.array(data, dtype="f4")

        return vertex_data

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)

        return vbo

    def get_shader_program(self, name):
        # parsing vertex shader
        with open(f"shaders/{name}.vert") as file:
            vertex_shader = file.read()

        # parsing fragment shader
        with open(f"shaders/{name}.frag") as file:
            fragment_shader = file.read()
        
        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        return program

    def get_vao(self):
        vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, "3f 3f 2f", "in_position", "in_color", "in_texcoord")])

        return vao

    def on_init(self):
        self.shader_program["tex0"] = 0
        self.texture.use()
        # adding the model, view, and projection matricies to the shader program
        self.shader_program["m_proj"].write(self.app.camera.m_proj)
        self.shader_program["m_view"].write(self.app.camera.m_view)
        self.shader_program["m_model"].write(self.m_model)

    def get_model_matrix(self):
        m_model = glm.mat4()
        return m_model
    
    def update(self):
        m_model = glm.rotate(self.m_model, pygame.time.get_ticks() * 0.001, glm.vec3(0, 0, 1))

        self.shader_program["m_model"].write(m_model)

    def render(self):
        self.update()

        self.vao.render()

    def destroy(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()
