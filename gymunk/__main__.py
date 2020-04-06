from . import Environment

import pygame
render = True
width = height = 500
env = Environment(width=width, height=height, render=render)

player = env.add_circle(20,20,50)
env.add_character(player)

for i in range(1000):
    state = env.step(1)
    if render:
        env.render()

pygame.quit() #hmm