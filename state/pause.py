import pygame, sys
from state.state import State
# from state.main_level import Level

class Pause(State):
    def __init__(self, game):
        State.__init__(self, game)

    def update(self, delta_time, keys, state_action):
        # print('In pause state')
        if state_action == 'start':
          self.game.state_stack.pop()

    def render(self, display):
        # display.fill((255,255,255))
        self.game.draw_text(display, "Paused", (255,255,255), 1280/2, 768/2 )