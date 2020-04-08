from . import Environment
from .action import SimpleDiscrete, CompoundDiscrete, SimpleContinuous

import pygame
render = True
width = height = 500
dt = 0.01
env = Environment(width=width, height=height, render=render, dt=dt, 
                    physics=SimpleContinuous)

player = env.add_circle(20,20,50)
obj = env.add_rect(100,50,10,10)
joint = env.add_pinjoint(player, obj)

env.add_character(player)
print(env.action_space)

for i in range(10000):
    action = env.debug_input()
    print(env.action_space.to_vec(action))
    state = env.step(action)
    if render:
        env.render()

pygame.quit() #hmm