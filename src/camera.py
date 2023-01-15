import glm
import pygame

FOV = 50 # deg
NEAR = 0.1
FAR = 100

SPEED = 0.02
SENSITIVITY = 0.09


class Camera:
    def __init__(self, app, position=(0, 0, 4), yaw=-90, pitch=0):
        self.app = app
        self.aspect_ratio = self.app.WIN_SIZE[0] / self.app.WIN_SIZE[1]

        # camera's position
        self.position = glm.vec3(position)
        
        # up vector
        self.up = glm.vec3(0, 1, 0)

        # right vector
        self.right = glm.vec3(1, 0, 0)

        # foward vector
        self.foward = glm.vec3(0, 0, -1)

        self.yaw = yaw

        self.pitch = pitch

        # view matrix
        self.m_view = self.get_view_matrix()

        # projection matrix
        self.m_proj = self.get_projection_matrix()
    
    def rotate(self):
        # getting the position of the mouse
        rel_x, rel_y = pygame.mouse.get_rel()

        # updating the yew and pitch values according to the mouse position and sensitivity
        self.yaw += rel_x * SENSITIVITY
        self.pitch -= rel_y * SENSITIVITY

        # setting a limit to the pitch value to prevent weird rotations
        self.pitch = max(-89, min(89, self.pitch))
    
    def update_camera_vectors(self):
        # converting the yew and pitch values to radians
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

        # calculating the new foward vector
        self.foward.x = glm.cos(yaw) * glm.cos(pitch)
        self.foward.y = glm.sin(pitch)
        self.foward.z = glm.sin(yaw) * glm.cos(pitch)

        self.foward = glm.normalize(self.foward)

        # calculating the new right and up vectors
        self.right = glm.normalize(glm.cross(self.foward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.foward))
    
    def move(self):
        # calculating the velocity taking delta time into account
        velocity = SPEED * self.app.delta_time
        keys = pygame.key.get_pressed()

        # checking for keyboard input and moving the camera accordingly
        if keys[pygame.K_w]:
            self.position += self.foward * velocity

        if keys[pygame.K_s]:
            self.position -= self.foward * velocity

        if keys[pygame.K_a] and not keys[pygame.K_d]:
            self.position -= self.right * velocity

        if keys[pygame.K_d] and not keys[pygame.K_a]:
            self.position += self.right * velocity

        if keys[pygame.K_q] and not keys[pygame.K_e]:
            self.position += self.up * velocity

        if keys[pygame.K_e] and not keys[pygame.K_q]:
            self.position -= self.up * velocity
    
    def update(self):
        # moving the camera
        self.move()

        # rotating the camera
        self.rotate()

        # updating the up, foward, and right vectors based on the current camera angle
        self.update_camera_vectors()

        # updating the view matrix
        self.m_view = self.get_view_matrix()

    def get_projection_matrix(self):
        # getting the projection matrix
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)
    
    def get_view_matrix(self):
        # getting the view matrix
        return glm.lookAt(self.position, self.position + self.foward, self.up)