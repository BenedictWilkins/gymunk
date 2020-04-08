import gym
import pygame


import pickle
import pygame
import pymunk
import pymunk.pygame_util

from . import utils
from .action import SimpleDiscrete

from pymunk import Body, Circle, Segment, Poly
from pymunk.constraint import PinJoint

pymunk.pygame_util.positive_y_is_up = False
pygame.init()

class GymunkError(Exception):
    pass


    
class Environment(gym.Env):

    DEFAULT_DENSITY = 0.0001

    def apply_force(body, force, point=(0,0)):
        body.apply_force_at_local_point(force, point)

    def __init__(self, width = 480, height = 480, dt=0.2, background_colour=(0,0,0), 
                render=False, physics=SimpleDiscrete):
        self.__render = render

        if render:
            self.surface = pygame.display.set_mode((width,height))
            pygame.display.set_caption("gymunk-" + self.__class__.__name__)
        else:
            self.surface = pygame.Surface((width,height))

        self.space = pymunk.Space()
        self.__draw_options = pymunk.pygame_util.DrawOptions(self.surface)
        self.background_colour = background_colour

        self.dt = dt

        self.bodies = []
        self.constraints = []
        self.characters = []

        self.__quit = False
        self.__events = {}

        self.action_physics = physics() #contains action_space
        print(self.action_physics)
        #self.observations_space = gym.spaces.Box(low=0, high=255) #TODO
    
    def action_to_vector(self, action):
        return self.action_physics.to_vec(action)

    def debug_input(self):
        """
            Get input from keyboard and return an action, this action may be used as an argument to env.step.
            Example Usage:
                env = gymunk.Environment(render=True)
                body = env.add_circle(100,100,40)
                env.add_character(body) #controlable 

                while True:
                    action = env.debug_input()
                    env.step(action)
                    env.render()
        
        Returns:
            [type]: [description]
        """
        assert self.__render
        return self.action_physics.debug_input()

    @property
    def action_space(self):
        return self.action_physics.action_space

    def step(self, action):
        self.surface.fill(self.background_colour)
        self.space.step(self.dt)
        self.space.debug_draw(self.__draw_options)
        self.action_physics.attempt(action, *self.characters)

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
    
    def add_constraint(self):
        raise NotImplementedError("TODO")

    def add_pinjoint(self, body1, body2, anchor_1=(0,0), anchor_2=(0,0)):
        joint = PinJoint(body1, body2, anchor_a=anchor_1, anchor_b=anchor_2)
        self.space.add(joint)
        self.constraints.append(joint)
        return joint

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
        assert self.__render # render must be set on initialisation
        if not self.__quit:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    self.__quit = True    
            pygame.display.update()
            #pygame.time.wait(int(1000 * self.dt)) #???
        else:
            raise GymunkError("Display has been closed, cannot render environment.")
