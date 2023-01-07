import numpy as np


class Triangle:
    def __init__(self, app):
        # an instance of the GraphicsEngine class
        self.app = app

        #self.vertex = vertex

        # the engine's OpenGL context
        self.ctx = self.app.ctx

        # vertex buffer object
        self.vbo = self.get_vbo()

        # shader program object
        self.shader_program = self.get_shader_program("default")

        # vertex array object
        self.vao = self.get_vao()
    
    def render(self):
        # rendering the model
        self.vao.render()
    
    def destroy(self):
        # destroying the model's resources (vertex buffer, vertex array, shader program, etc) because OpenGL has no garbage collector
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()

    def get_vao(self):
        # VAO - vertex array object (associating vertex buffer with the shader program)
        vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, "3f 3f", "in_position", "in_color")])

        # returning the vertex array object
        return vao
    
    def get_vertex_data(self):
        # vertex data of the triangle. (An aray of XYZ coordinates of each vertex and the RGB values)
        #vertex_data = [(-0.6, -0.8, 0.0, 0.6, -0.8, 0.0, 0.0, 0.8, 0.0), (0.1, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.1)] 
        vertex_data = [
            (-0.6, -0.8, 0.0, 0.5, 0.0, 0.0), 
            (0.6, -0.8, 0.0, 0.0, 0.5, 0.0),
            (0.0, 0.8, 0.0, 0.0, 0.0, 0.5)
            ]

        # converting the vertex data to a numpy array that can be used by OpenGL
        vertex_data = np.array(vertex_data, dtype="f4")

        # returning the vertex data
        return vertex_data

    def get_vbo(self):
        vertex_data = self.get_vertex_data()

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
    