import pygame, sys
from pytmx.util_pygame import load_pygame
from pygame.math import Vector2 as vector
from state.level.settings import *
from state.title import Title

class Main:
  def __init__(self):
    pygame.init()
    self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    self.game_window = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Endless Runner')
    self.state_stack = []
    self.state_action = None
    self.keys = None
    self.clock = pygame.time.Clock()
    self.dt = 0
    self.load_states()
    self.font= pygame.font.SysFont('Ariel', 24)

  def load_states(self):
    self.title_screen = Title(self)
    self.state_stack.append(self.title_screen)

  def get_dt(self):
    self.dt = self.clock.tick() / 1000

  def update(self):
    self.keys =  pygame.key.get_pressed()
    self.state_stack[-1].update(self.dt, self.keys, self.state_action)

  def render(self):
    self.state_stack[-1].render(self.game_window)
    self.display_surface.blit(self.game_window,(0, 0))
    pygame.display.update()

  def draw_text(self, surface, text, color, x, y):
    text_surface = self.font.render(text, True, color)
    #text_surface.set_colorkey((0,0,0))
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)

  def run(self):
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            if self.state_action == 'pause':
              self.state_action = 'start'
            elif self.state_action == 'start':
              self.state_action = 'pause'
          if event.key == pygame.K_RETURN:
            self.state_action = 'start'

      self.get_dt()
      self.update()
      self.render()

if __name__ == '__main__':
	main = Main()
	main.run()