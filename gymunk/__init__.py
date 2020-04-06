import gym
import pygame

import pygame
import pymunk
import pymunk.pygame_util

from pymunk import Body, Circle, Segment, Poly
from pymunk.constraint import PinJoint

pymunk.pygame_util.positive_y_is_up = False
pygame.init()

class GymunkError(Exception):
    pass

class Environment(gym.Env):

    DEFAULT_DENSITY = 0.0001
    CHARACTER_CONTROLS = [lambda body: Environment.apply_force(body, (-1,0)),
                          lambda body: Environment.apply_force(body, (1,0)),
                          lambda body: Environment.apply_force(body, (0,-1)),
                          lambda body: Environment.apply_force(body, (0,1))]


    def apply_force(body, force, point=(0,0)):
        body.apply_force_at_local_point(force, point)

    def __init__(self, width = 480, height = 480, dt=0.2, background_colour=(0,0,0), render=False):
        self.space = pymunk.Space()
        self.surface = pygame.Surface((width,height))
        self.__draw_options = pymunk.pygame_util.DrawOptions(self.surface)
        
        self.dt = dt
        
        self.bodies = []
        self.characters = []

        self.__quit = False
        self.__events = {}

        if render:
            self.__display = pygame.display.set_mode((width,height))
            pygame.display.set_caption("gymunk-" + self.__class__.__name__)
    
    def step(self, action):
        self.space.step(self.dt)
        self.space.debug_draw(self.__draw_options)
        for character in self.characters:
            Environment.CHARACTER_CONTROLS[action](character)

        return self.get_image_raw(), self.reward(action), False, None

    def reward(self, action):
        return 0.

    def get_image_raw(self):
        return pygame.surfarray.array3d(self.surface)

    def reset(self):
        pass


    def add_character(self, body):
        if body not in self.space.bodies:
            self.space.add(body, *body.shapes)
        self.characters.append(body)

    def add_body(self, body):
        self.space.add(body, *body.shapes)
        self.bodies.append(body)
        return body

    def add_segment(self, x1,y1,x2,y2, thickness=1, dynamic=True):
        body = Body(body_type=(Body.STATIC, Body.DYNAMIC)[int(dynamic)])
        seg = Segment(body,(x1,y1),(x2, y2),radius=thickness)
        seg.density = Environment.DEFAULT_DENSITY
        self.space.add(body, seg)
        self.bodies.append(body)
        return body

    def add_circle(self, x, y, r, dynamic=True):
        body = Body(body_type=(Body.STATIC, Body.DYNAMIC)[int(dynamic)])
        body.position = x, y
        circle = Circle(body, r)
        circle.density = Environment.DEFAULT_DENSITY
        self.space.add(body, circle)
        self.bodies.append(body)
        return body

    def add_rect(self, x, y, w, h, dynamic=True):
        body = Body(body_type=(Body.STATIC, Body.DYNAMIC)[int(dynamic)])
        body.position = x, y
        poly = Poly.create_box(body, size=(w,h))
        poly.density = Environment.DEFAULT_DENSITY
        self.space.add(body, poly)
        self.bodies.append(body)
        return body

    def add_polygon(self, x, y, *vertices, dynamic=True):
        body = Body(body_type=(Body.STATIC, Body.DYNAMIC)[int(dynamic)])
        body.position = x, y
        poly = Poly(body, vertices)
        poly.density = Environment.DEFAULT_DENSITY
        self.space.add(body, poly)
        self.bodies.append(body)
        return body

    

    @property
    def size(self):
        return self.surface.get_size()

    def render(self, *args, **kwargs): 
        if not self.__quit:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    self.__quit = True    
            
            self.__display.blit(self.surface, (0,0))
            pygame.display.update()
            pygame.time.wait(100)
        else:
            raise GymunkError("Display has been closed, cannot render environment.")
