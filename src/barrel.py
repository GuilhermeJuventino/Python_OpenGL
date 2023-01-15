import pygame
import numpy as np
import glm

from model_3d import *


class Barrel:
    def __init__(self, app):
        # an instance of the GraphicsEngine class
        self.app = app

        #self.vertex = vertex

        # the engine's OpenGL context
        self.ctx = self.app.ctx

        self.model = Model3D("models/Wooden Barrel.obj")
        #self.model = Model3D("models/12221_Cat_v1_l3.obj")

        self.texture_wood = self.get_texture("textures/Wood Diffuse.jpg")
        #self.texture_metal = self.get_texture("textures/Metal Diffuse.jpg")
        #self.texture = self.get_texture("textures/Cat_diffuse.jpg")

        # vertex buffer object
        self.vbo = self.get_vbo()

        # shader program object
        self.shader_program = self.get_shader_program("default")

        # vertex array object
        self.vao = self.get_vao()

        # model matrix
        self.m_model = self.get_model_matrix()

        self.on_init()
    
    def get_texture(self, path):
        texture = pygame.image.load(path).convert()
        texture = pygame.transform.flip(texture, flip_x=False, flip_y=True)

        texture = self.ctx.texture(size=texture.get_size(), components = 3,
        data=pygame.image.tostring(texture, "RGB"))

        return texture
    
    def render(self):
        # updating the model
        self.update()

        # rendering the model
        self.vao.render()
    
    def on_init(self):
        self.shader_program["uv_0"] = 0
        self.texture_wood.use()
        #self.texture.use()
        # adding the model, view, and projection matricies to the vertex shader
        self.shader_program["m_proj"].write(self.app.camera.m_proj)
        self.shader_program["m_view"].write(self.app.camera.m_view)
        self.shader_program["m_model"].write(self.m_model)
    
    def get_model_matrix(self):
        # getting the model matrix
        m_model = glm.mat4()
        return m_model
    
    def update(self):
        # rotating the model matrix
        m_model = glm.rotate(self.m_model, pygame.time.get_ticks() * 0.001, glm.vec3(1, 0, 0))
        
        # sending the updated model matrix to the vertex shader
        self.shader_program["m_model"].write(m_model)
        self.shader_program["m_view"].write(self.app.camera.m_view)
    
    def destroy(self):
        # destroying the model's resources (vertex buffer, vertex array, shader program, etc) because OpenGL has no garbage collector
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()

    def get_vao(self):
        # VAO - vertex array object (associating vertex buffer with the shader program)
        vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, self.model.format, self.model.attributes[0],
        self.model.attributes[1], self.model.attributes[2])])

        # returning the vertex array object
        return vao
    
    """def get_vertex_data(self):
        # vertex data of the triangle. (An aray of XYZ coordinates of each vertex and the RGB values)
        #vertex_data = [(-0.6, -0.8, 0.0, 0.6, -0.8, 0.0, 0.0, 0.8, 0.0), (0.1, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.1)] 

        vertex_data

        # returning the vertex data
        return vertex_data"""

    def get_vbo(self):
        vertex_data = self.model.get_vertex_data()

        # VBO - vertex buffer object (Sending the vertex data to the GPU)
        vbo = self.ctx.buffer(vertex_data)

        # returning the vertex buffer object
        return vbo
    
    def get_shader_program(self, shader_name):
        # loading data from vertex shader
        with open(f"shaders/{shader_name}.vert") as file:
            vertex_shader = file.read()
        
        # loading data from fragment shader
        with open(f"shaders/{shader_name}.frag") as file:
            fragment_shader = file.read()
        
        # creating shader program object
        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        # returning the shader program object
        return program