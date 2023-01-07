import pygame
import moderngl as mgl
from sys import exit

from model import *


class GraphicsEngine:
    def __init__(self, win_size=(1600, 900)):
        # initialize pygame
        self.WIN_SIZE = win_size
        pygame.init()
        
        # setting OpgenGL attributes
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

        # creating OpenGL context
        pygame.display.set_mode(self.WIN_SIZE, flags=pygame.OPENGL | pygame.DOUBLEBUF)

        # detecting OpenGL context
        self.ctx = mgl.create_context()

        # creating an object to track time
        self.clock = pygame.time.Clock()

        #vertex_data_1 = [(-0.6, -0.8, 0.0), (0.6, -0.8, 0.0), (0.6, 0.8, 0.0)]
        #vertex_data_2 = [(-0.6, -0.8, 0.0), (0.6, 0.8, 0.0), (-0.6, 0.8, 0.0)]

        # scene
        self.scene = Triangle(self)
        #self.triangle_1 = Triangle(self, vertex_data_1)
        #self.triangle_2 = Triangle(self, vertex_data_2)
    
    def check_events(self):
        # event loop
        for event in pygame.event.get():

            # checking if the program should close
            if event.type == pygame.QUIT:
                self.scene.destroy()
                pygame.quit()
                exit()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.scene.destroy()
                pygame.quit()
                exit()
    
    def destroy_all(self):
        pass
            
    def render(self):
        # clear framebuffer (Clearing the screen)
        self.ctx.clear(color=(0.08, 0.16, 0.18))

        # rendering stuff
        self.scene.render()
        #self.triangle_1.render()
        #self.triangle_2.render()

        # changing the title of the window, and displaying the current framerate
        pygame.display.set_caption(f"Pygame OpenGL - FPS: {self.clock.get_fps() :.1f}")

        # swapping buffers (updating the screen)
        pygame.display.flip()
     
    def run(self):
        # main loop
        while True:
            # checking for events every frame
            self.check_events()

            # updating and drawing every frame
            self.render()

            # set framerate
            self.clock.tick(60)


if __name__ == "__main__":
    # creating an instance of the engine
    app = GraphicsEngine()

    app.run()
