import pygame
import gym

import numpy as np

from . import utils

class SimpleDiscrete:

    __effects__ = [lambda body : None,  #NULL
                   lambda body: body.apply_force_at_local_point((0,-1), (0,0)), #UP
                   lambda body: body.apply_force_at_local_point((1,0), (0,0)),  #RIGHT
                   lambda body: body.apply_force_at_local_point((0,1), (0,0)),  #DOWN
                   lambda body: body.apply_force_at_local_point((-1,0), (0,0))] #LEFT

    __action_space__ = utils.InformativeActionSpace(gym.spaces.Discrete, 
                                                {0:'NULL - force (0,0)',
                                                 1:'UP - force (0,-1)',
                                                 1:'LEFT - force (-1,0)',
                                                 2:'RIGHT - force (1,0)',
                                                 4:'DOWN - force (0,1)'},
                                                 utils.onehotter(5))(5)
    
    def __init__(self, *args, **kwargs):
        super(SimpleDiscrete, self).__init__(*args, **kwargs)
        self.action_space = SimpleDiscrete.__action_space__

    def attempt(self, action, *characters):
        for c in characters:
            SimpleDiscrete.__effects__[action](c) #apply the force to each character

    def debug_input(self):
        keys=pygame.key.get_pressed()
        # yes, there is a priority, see CompoundDiscrete if you dont like this
        if keys[pygame.K_UP]:
            return 1
        if keys[pygame.K_RIGHT]:
            return 2
        if keys[pygame.K_DOWN]:
            return 3
        if keys[pygame.K_LEFT]:
            return 4
        return 0

class CompoundDiscrete:

    __effects__ = [lambda body: None,  #NULL
                   lambda body: body.apply_force_at_local_point((0,-1), (0,0)), #UP
                   lambda body: body.apply_force_at_local_point((1,-1), (0,0)), #UP_RIGHT
                   lambda body: body.apply_force_at_local_point((1,0), (0,0)),  #RIGHT
                   lambda body: body.apply_force_at_local_point((1,1), (0,0)),  #DOWN_RIGHT
                   lambda body: body.apply_force_at_local_point((0,1), (0,0)),  #DOWN
                   lambda body: body.apply_force_at_local_point((-1,1), (0,0)), #DOWN_LEFT
                   lambda body: body.apply_force_at_local_point((-1,0), (0,0)), #LEFT
                   lambda body: body.apply_force_at_local_point((-1,-1), (0,0))] #UP_LEFT
                  

    __action_space__ = utils.InformativeActionSpace(gym.spaces.Discrete, 
                                                {0:'NULL - force (0,0)',
                                                 1:'UP - force (0,-1)',
                                                 2:'UP_RIGHT - force (1,-1)',
                                                 3:'RIGHT - force (1,0)',
                                                 4:'DOWN_RIGHT - force (1,1)',
                                                 5:'DOWN - force (0,1)',
                                                 6:'DOWN_LEFT (-1,1)',
                                                 7:'LEFT - force (-1,0)',
                                                 8:'UP_LEFT - force (-1,-1)'},
                                                 utils.onehotter(9))(9)

    __inverse__ =  {(0,0):0, (0,-1):1, (1,-1):2, (1,0):3, (1,1):4, (0,1):5, (-1,1):6, (-1,0):7, (-1,-1):8}                                          
    
    
    def __init__(self, scale=1, *args, **kwargs):
        super(CompoundDiscrete, self).__init__(*args, **kwargs)
        self.action_space = CompoundDiscrete.__action_space__
        self.scale = scale #TODO

    def attempt(self, action, *characters):
        for c in characters:
            CompoundDiscrete.__effects__[action](c) #apply the force to each character

    def debug_input(self):
        keys=pygame.key.get_pressed()
        x = y = 0
        if keys[pygame.K_UP]:
            y -= 1
        if keys[pygame.K_RIGHT]:
            x += 1
        if keys[pygame.K_DOWN]:
            y += 1
        if keys[pygame.K_LEFT]:
            x -= 1
        return CompoundDiscrete.__inverse__[(x,y)]

class CompactVectorSpace(gym.spaces.Space):

    def __init__(self, size, bounds, action_meaning):
        assert isinstance(size, int)
        assert len(bounds) == size
        super(CompactVectorSpace, self).__init__(shape=(size,), dtype=np.float32)
        self.bounds = bounds
        self.action_meaning = action_meaning

    def contains(self, x):
        all(self.bounds[i][0] <= x[i] <= self.bounds[i][1] for i in range(self.shape[0]))

    def to_vec(self, x):
        return np.array(x) #it should already be a vector-like type
        
    
class SimpleContinuous:    

    __action_space__ = CompactVectorSpace(2, [(-1,1),(-1,1)], "Continuous actions (x,y) will apply a force at the center of a character.")

    def __init__(self, *args, **kwargs):
        super(SimpleContinuous, self).__init__(*args, **kwargs)
        self.action_space = SimpleContinuous.__action_space__

    def attempt(self, action, *characters):
        for c in characters:
            c.apply_force_at_local_point(action, (0,0))

    def debug_input(self):
        keys=pygame.key.get_pressed()
        x = y = 0
        if keys[pygame.K_UP]:
            y -= 1
        if keys[pygame.K_RIGHT]:
            x += 1
        if keys[pygame.K_DOWN]:
            y += 1
        if keys[pygame.K_LEFT]:
            x -= 1
        xy = np.sqrt(x ** 2 + y ** 2)
        if xy > 0:
            return (x/xy,y/xy)
        else:
            return (x, y)#(0,0)
       