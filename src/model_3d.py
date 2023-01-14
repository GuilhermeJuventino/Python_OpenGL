import numpy as np
import pywavefront


class Model3D:
    def __init__(self, path):
        # path to the .obj model
        self.path = path

        # the format of vertex array
        self.format = "2f 3f 3f"

        # the attributes of the vertex array
        self.attributes = ["in_texcoord_0", "in_normal", "in_position"]

    # getting the vertex data from the .obj model
    def get_vertex_data(self):
        # loading the .obj model
        model = pywavefront.Wavefront(self.path, parse=True, cache=True)
        obj = model.materials.popitem()[1]

        # getting the vertex data from model
        vertex_data = obj.vertices

        # converting the vertex data to a structure that can be read by OpenGL
        vertex_data = np.array(vertex_data, dtype="f4")

        # returning the vertex data
        return vertex_data
