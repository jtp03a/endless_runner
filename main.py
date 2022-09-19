import pygame, sys
from pytmx.util_pygame import load_pygame
from pygame.math import Vector2 as vector
from player import Player
from enemy import Enemy
from settings import *
from tile import Tile
import random
from camera import *


class AllSprites(pygame.sprite.Group):
  def __init__(self):
    super().__init__()
    self.display_surface = pygame.display.get_surface()
       
    # layer setup
    self.ground = pygame.image.load('./graphics/background/1.png').convert_alpha()
    self.forground = pygame.image.load('./graphics/background/0.png').convert_alpha()
    self.canopy = pygame.image.load('./graphics/background/2.png').convert_alpha()
    self.trees1 = pygame.image.load('./graphics/background/3.png').convert_alpha()
    self.lights1 = pygame.image.load('./graphics/background/4.png').convert_alpha()
    self.trees2 = pygame.image.load('./graphics/background/5.png').convert_alpha()
    self.trees3 = pygame.image.load('./graphics/background/6.png').convert_alpha()
    self.lights2 = pygame.image.load('./graphics/background/7.png').convert_alpha()
    self.trees4 = pygame.image.load('./graphics/background/8.png').convert_alpha()
    self.BG1 = pygame.image.load('./graphics/background/9.png').convert_alpha()
    self.BG2 = pygame.image.load('./graphics/background/10.png').convert_alpha()
    self.BG3 = pygame.image.load('./graphics/background/11.png').convert_alpha()

    # layer groups
    self.ground_sprites = pygame.sprite.Group()
    self.forground_sprites = pygame.sprite.Group()
    self.trees1_sprites = pygame.sprite.Group()
    self.canopy_sprites = pygame.sprite.Group()
    self.lights1_sprites = pygame.sprite.Group()
    self.trees2_sprites = pygame.sprite.Group()
    self.trees3_sprites = pygame.sprite.Group()
    self.lights2_sprites = pygame.sprite.Group()
    self.trees4_sprites = pygame.sprite.Group()
    self.BG1_sprites = pygame.sprite.Group()
    self.BG2_sprites = pygame.sprite.Group()
    self.BG3_sprites = pygame.sprite.Group()
    self.collision_sprites = pygame.sprite.Group()


    self.layer_setup(self.ground, [self.ground_sprites, self.collision_sprites], 'Ground')
    self.layer_setup(self.forground, self.forground_sprites, 'FG')
    self.layer_setup(self.canopy, self.canopy_sprites, 'Canopy')
    self.layer_setup(self.trees1, self.trees1_sprites, 'Trees1')
    self.layer_setup(self.lights1, self.lights1_sprites, 'Lights1')
    self.layer_setup(self.trees2, self.trees2_sprites, 'Trees2')
    self.layer_setup(self.trees3, self.trees3_sprites, 'Trees3')
    self.layer_setup(self.lights2, self.lights2_sprites, 'Lights2')
    self.layer_setup(self.trees4, self.trees4_sprites, 'Trees4')
    self.layer_setup(self.BG1, self.BG1_sprites, 'BG1')
    self.layer_setup(self.BG2, self.BG2_sprites, 'BG2')
    self.layer_setup(self.BG3, self.BG3_sprites, 'BG3')
    
  def setup_camera(self, player):
    self.camera = Camera(player)
    self.follow = Follow(self.camera, player)
    self.auto = Auto(self.camera, player)
    self.border = Border(self.camera, player)
    self.box = Box(self.camera, player)
    self.camera.setmethod(self.box)

  def layer_setup(self, surf, group, layer):
    # for x in range(self.calc_tiles(surf)):
      Tile((0 * surf.get_width(), -130), surf, group, layer)
      Tile((1 * surf.get_width(), -130), surf, group, layer)

  def infinite_tiles(self, group, layer, scroll_speed, groups):
    for i, sprite in enumerate(group):
      offset = self.camera.offset.x / scroll_speed
      self.display_surface.blit(sprite.image, (sprite.rect.left - offset - 200, -130 - self.camera.offset.y))
      difference = offset - sprite.rect.right
      if difference > 0:
        sprite.kill()
      if len(group.sprites()) < 3:
          Tile((group.sprites()[-1].rect.right, -130), sprite.image, groups, layer)
  
  def custom_draw(self):

    self.camera.scroll()

    self.infinite_tiles(self.BG3_sprites, 'BG3', 3.0, self.BG3_sprites)
    self.infinite_tiles(self.BG2_sprites, 'BG2', 3.0, self.BG2_sprites)
    self.infinite_tiles(self.BG1_sprites, 'BG1', 3.0, self.BG1_sprites)
    self.infinite_tiles(self.trees4_sprites, 'Trees4', 2.5, self.trees4_sprites)
    self.infinite_tiles(self.lights2_sprites, 'Lights2', 2.2, self.lights2_sprites)
    self.infinite_tiles(self.trees3_sprites, 'Trees3', 2.0, self.trees3_sprites)
    self.infinite_tiles(self.trees2_sprites, 'Trees2', 1.7, self.trees2_sprites)
    self.infinite_tiles(self.lights1_sprites, 'Lights1', 1.5, self.lights1_sprites)
    self.infinite_tiles(self.trees1_sprites, 'Trees1', 1.2, self.trees1_sprites)
    self.infinite_tiles(self.canopy_sprites, 'Canopy', 1.2, self.canopy_sprites)
    self.infinite_tiles(self.ground_sprites, 'Ground', 1.0, [self.ground_sprites, self.collision_sprites])

    # pygame.draw.rect(self.display_surface, 'red', sprite.mask_rect, 5)

    # active elements
    for sprite in sorted(self.sprites(), key = lambda sprite: sprite.z):
      self.display_surface.blit(sprite.image, (sprite.rect.x - self.camera.offset.x, sprite.rect.y - self.camera.offset.y))

    self.infinite_tiles(self.forground_sprites, 'FG', .8, self.forground_sprites)

class Main:
  def __init__(self):
    pygame.init()
    self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Endless Runner')
    self.clock = pygame.time.Clock()
    self.enemy_time = pygame.time.get_ticks()
    self.random_interval = random.randint(1000, 5000)
    self.gen_enemy = False
    self.gen_enemies()

    self.all_sprites = AllSprites()

    self.player = Player((0, 478), self.all_sprites, self.all_sprites.collision_sprites)

    self.all_sprites.setup_camera(self.player)

  def gen_enemies(self):
    current_time = pygame.time.get_ticks()

    if current_time - self.enemy_time > self.random_interval:
      Enemy((random.randint(int(self.player.pos.x - 200), int(self.player.pos.x + 200)), 200), self.all_sprites, self.all_sprites.collision_sprites)
      self.random_interval = random.randint(1000, 5000)
      self.enemy_time = pygame.time.get_ticks()

  def run(self):
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()

      dt = self.clock.tick() / 1000
      self.display_surface.fill((12,17,34))
      self.all_sprites.update(dt, self.all_sprites.camera.camera_rect.left)
      self.all_sprites.custom_draw()
      self.gen_enemies()
      pygame.display.update()

if __name__ == '__main__':
	main = Main()
	main.run()