import pygame, sys
from state.state import State
from state.main_level import Level

class Title(State):
    def __init__(self, game):
        State.__init__(self, game)
        
    def update(self, delta_time, keys, state_action):
        if state_action == 'start':
            new_state = Level(self.game)
            new_state.enter_state()

    def render(self, display):
        display.fill((255,255,255))
        self.game.draw_text(display, "Game States Demo", (0,0,0), 1280/2, 768/2 )