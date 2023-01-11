import glm

FOV = 50 # deg
NEAR = 0.1
FAR = 100


class Camera:
    def __init__(self, app):
        self.app = app
        self.aspect_ratio = self.app.WIN_SIZE[0] / self.app.WIN_SIZE[1]

        # camera's position
        self.position = glm.vec3(2, 3, 3)
        
        # up vector
        self.up = glm.vec3(0, 1, 0)

        # view matrix
        self.m_view = self.get_view_matrix()

        # projection matrix
        self.m_proj = self.get_projection_matrix()

    def get_projection_matrix(self):
        # getting the projection matrix
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)
    
    def get_view_matrix(self):
        # getting the view matrix
        return glm.lookAt(self.position, glm.vec3(0), self.up)