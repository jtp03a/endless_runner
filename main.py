import pygame, sys
from pytmx.util_pygame import load_pygame
from pygame.math import Vector2 as vector
from player import Player
from enemy import Enemy
from settings import *
import random
from state.level import AllSprites
from state.title import Title


class Main:
  def __init__(self):
    pygame.init()
    self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    self.game_window = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Endless Runner')
    self.state_stack = []
    self.actions = []
    self.clock = pygame.time.Clock()
    self.dt = 0
    self.load_states()
    self.font= pygame.font.SysFont('Ariel', 24)
    self.enemy_time = pygame.time.get_ticks()
    self.random_interval = random.randint(1000, 5000)
    self.gen_enemy = False
    # self.gen_enemies()

    # self.all_sprites = AllSprites()
    # self.dead_sprites = pygame.sprite.Group()

    # self.player = Player((0, 478), self.all_sprites, self.all_sprites.collision_sprites)

    # self.all_sprites.setup_camera(self.player)

  def gen_enemies(self):
    current_time = pygame.time.get_ticks()

    if current_time - self.enemy_time > self.random_interval:
      Enemy((random.randint(int(self.player.pos.x - 200), int(self.player.pos.x + 200)), 200), self.all_sprites, self.all_sprites.collision_sprites, self.player)
      self.random_interval = random.randint(1000, 5000)
      self.enemy_time = pygame.time.get_ticks()

  def damage(self):
    for sprite in self.all_sprites.sprites():
      if pygame.sprite.collide_mask(self.player, sprite) and not sprite.is_player and self.player.attacking and not sprite.dying:
        sprite.dying = True
        self.dead_sprites.add(sprite)
        sprite.direction.x = 0
        sprite.frame_index = 0

  def remove_dead_sprites(self):
    for sprite in self.dead_sprites.sprites():
      if self.player.pos.x - sprite.pos.x > WINDOW_WIDTH:
        sprite.kill() 

  def load_states(self):
    self.title_screen = Title(self)
    self.state_stack.append(self.title_screen)

  def get_dt(self):
    self.dt = self.clock.tick() / 1000

  def update(self):
    self.state_stack[-1].update(self.dt, self.actions)

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

      self.get_dt()
      self.update()
      self.render()
      # self.display_surface.fill((12,17,34))

      # self.all_sprites.update(self.dt, self.all_sprites.camera.camera_rect.left)
      # self.damage()
      # self.remove_dead_sprites()
      # self.all_sprites.custom_draw()
      # self.gen_enemies()
      # pygame.display.update()

if __name__ == '__main__':
	main = Main()
	main.run()