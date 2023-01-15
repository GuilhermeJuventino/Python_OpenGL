import glm


class Light:
    def __init__(self, position=(3, 3, -3), color=(1, 1, 1)):
        # light source's position
        self.pos = glm.vec3(position)

        # light source's color
        self.color = glm.vec3(color)


        # light intensities

        # ambient lighting
        self.Ia = 0.1 * self.color

        # diffuse lighting
        self.Id = 0.8 * self.color

        # specular lighting
        self.Is = 1.0 * self.color
