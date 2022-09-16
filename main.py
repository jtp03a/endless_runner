from re import L, T
import pygame, sys
from pytmx.util_pygame import load_pygame
from pygame.math import Vector2 as vector
from player import Player
from settings import *
from tile import Tile
import math
from camera import *

class AllSprites(pygame.sprite.Group):
  def __init__(self):
    super().__init__()
    # self.offset = vector()
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


    self.layer_setup(self.ground, [self.ground_sprites, self, self.collision_sprites], 'Ground')
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
    
    # zoom logic
    # self.zoom_scale = 1
    # self.internal_surface_size = (1280, 768)
    # self.internal_surface = pygame.Surface(self.internal_surface_size, pygame.SRCALPHA)
    # self.internal_rect = self.internal_surface.get_rect(center = (WINDOW_WIDTH * .5, WINDOW_HEIGHT * .5))
    # self.internal_surface_size_vector = vector(self.internal_surface_size)
    # self.internal_offset = vector(0,0)
    # self.internal_offset.x = self.internal_surface_size[0] // 2 - WINDOW_WIDTH * .5
    # self.internal_offset.y = self.internal_surface_size[1] //2 - WINDOW_HEIGHT * .5

  # def zoom_keyboard(self):
  #   keys = pygame.key.get_pressed()
  #   if keys[pygame.K_q]:
  #     self.zoom_scale += 0.01
  #   if keys[pygame.K_e]:
  #     self.zoom_scale -= 0.01

  # def calc_tiles(self, surf):
  #   width = surf.get_width()
  #   tiles = math.ceil(WINDOW_WIDTH / width)
  #   return tiles

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
  
  def custom_draw(self, player):

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
    self.infinite_tiles(self.ground_sprites, 'Ground', 1.0, [self.ground_sprites, self.collision_sprites, self])

    
    # for sprite in self.ground_sprites:
    #   pygame.draw.rect(self.display_surface, 'red', sprite.mask_rect, 5)

    self.display_surface.blit(player.image, (player.rect.x - self.camera.offset.x, player.rect.y - self.camera.offset.y))

    self.infinite_tiles(self.forground_sprites, 'FG', .8, self.forground_sprites)

    # active elements
    # for sprite in sorted(self.sprites(), key = lambda sprite: sprite.z):
    #   offset_rect = sprite.image.get_rect(center = sprite.rect.center)
    #   offset_rect.center -= self.offset
    #   self.display_surface.blit(sprite.image, offset_rect)

    # zoom logic
      # self.zoom_keyboard()
    # self.internal_surface.fill((100,255,255))
    # scaled_surf = pygame.transform.scale(self.internal_surface, self.internal_surface_size_vector * self.zoom_scale)
    # scaled_rect = scaled_surf.get_rect(center = (WINDOW_WIDTH * .5, WINDOW_HEIGHT * .5))

    # self.display_surface.blit(scaled_surf, scaled_rect)
      

class Main:
  def __init__(self):
    pygame.init()
    self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Endless Runner')
    self.clock = pygame.time.Clock()

    self.all_sprites = AllSprites()

    self.player = Player((0, 478), self.all_sprites, self.all_sprites.collision_sprites)

    self.all_sprites.setup_camera(self.player)

  def run(self):
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()

      dt = self.clock.tick() / 1000
      self.display_surface.fill((12,17,34))
      self.all_sprites.update(dt, self.all_sprites.camera.camera_rect.left)
      self.all_sprites.custom_draw(self.player)
      
      pygame.display.update()

if __name__ == '__main__':
	main = Main()
	main.run()