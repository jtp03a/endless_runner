import pygame
from spritesheet import SpriteSheet
from settings import *
from os import walk
from pygame.math import Vector2 as vector
import math

class Enemy(pygame.sprite.Sprite):
  def __init__(self, pos, groups, collision_sprites, player):
    super().__init__(groups)
    self.player = player
    self.import_assets('./graphics/enemy')
    self.status = 'Right_Idle'
    self.frame_index = 0
    self.image = self.anim_dict[self.status.split('_')[1]][self.frame_index]
    self.z = 1

    # self.mask = pygame.mask.from_surface(self.image)
    # self.mask_rect = self.mask.get_rect(bottomleft = pos)
    self.rect = self.image.get_rect(topleft = pos)
    # float based movement
    self.pos = vector(self.rect.center)
    self.direction = vector(0, 0)
    self.speed = 400

    self.attacking = False

    self.collision_sprites = collision_sprites
    self.collision_rect = self.rect.inflate(self.rect.width, self.rect.height * .75)
    self.prev_rect = self.rect.copy()

    
    self.gravity = 15
    self.on_floor = True
    self.is_player = False
    self.dead = False
    self.dying = False

  def import_assets(self, path):
    self.anim_dict = {}
    self.asset_direction = ['Right', 'Left']
    for index, folder in enumerate(walk(path)):
      for file in folder[2]:
        file_name = file.split('.')[0]
        num_frames = ENEMY_POS[file_name][2]
        start_x = ENEMY_POS[file_name][0]
        start_y = ENEMY_POS[file_name][1]
        rect_w = ENEMY_POS[file_name][3]
        rect_h = ENEMY_POS[file_name][4]
        self.spritesheet = SpriteSheet(f'./graphics/enemy/{file}')
        self.anim_dict[file_name] = []
        for _ in range(num_frames):
          new_image = self.spritesheet.image_at((start_x, start_y, rect_w, rect_h), colorkey=(255, 255, 255))
          self.anim_dict[file_name].append(new_image)
          start_x += 200  
  
  def get_status(self):  
    # idle
    if self.direction.x == 0 and not self.attacking:
      self.status = self.status.split('_')[0] + '_Idle'

    # attacking
    if self.attacking:
      self.status = self.status.split('_')[0] + '_Attack'

    # jumping
    # if self.direction.y < 0 and not self.on_floor:
    #   self.status = self.status.split('_')[0] + '_Jump'
    # if self.direction.y > 0 and not self.on_floor:
    #   self.status = self.status.split('_')[0] + '_Fall'

    # # ducking
    # if self.ducking and self.on_floor:
    #   self.status = self.status.split('_')[0] + '_duck'

    # death
    if self.dying:
      self.status = self.status.split('_')[0] + '_Death'


  def animate(self, dt):
    if not self.dead:
      current_animation = self.anim_dict[self.status.split('_')[1]]

      if self.attacking and self.status.split('_')[0] == 'Left':
        x_pos = self.rect.bottomleft[0] + self.anim_dict['Idle'][0].get_width()
        self.rect = current_animation[int(self.frame_index)].get_rect(bottomright = (x_pos, self.rect.bottomleft[1]))

      self.frame_index += 7 * dt 

      if self.frame_index >= len(current_animation):
        self.frame_index = 0
        if self.dying:
          self.dead = True
          self.direction.x = 0

      if self.dead:
        self.frame_index = len(current_animation) -1
      # else:
      #   self.frame_index = len(current_animation)
        # if self.attacking:
        #   self.attacking = False

      self.image = current_animation[int(self.frame_index)]
    else:
      pass

  # def check_floor_contact(self):
  #   bottom_rect = pygame.Rect(0,0,self.rect.width,5)
  #   bottom_rect.midtop = self.rect.midbottom
  #   for sprite in self.collision_sprites.sprites():
  #     if sprite.rect.colliderect(bottom_rect):
  #       if self.direction.y > 0:
  #         self.on_floor = True

  def collision(self, direction):
    for sprite in self.collision_sprites.sprites():
      if sprite.rect.colliderect(self.rect):
        if direction == 'horizontal':
          # left collision
          if self.rect.left <= sprite.rect.right and self.prev_rect.left >= sprite.prev_rect.right:
            self.rect.left = sprite.rect.right
          # right collision
          if self.rect.right >= sprite.rect.left and self.prev_rect.right <= sprite.prev_rect.left:
            self.rect.right = sprite.rect.left
          self.pos.x = self.rect.x
        elif direction == 'vertical': 
          # top collision
          if self.rect.top <= sprite.rect.bottom and self.prev_rect.top >= sprite.prev_rect.bottom:
            self.rect.top = sprite.rect.bottom
          # bottom collision
          if self.rect.bottom >= sprite.mask_rect.top:
            self.rect.bottom = sprite.mask_rect.top
            self.on_floor = True
            self.direction.y = 0
          self.pos.y = self.rect.y

     # check if the player is falling
    if self.on_floor and self.direction.y != 0:
      self.on_floor = False
      

  def move(self, dt):  
    # Horizontal movement + collision
    # self.direction.x = 0.25
    if self.on_floor and not self.dead and abs(self.player.pos.x - self.pos.x) > 50:
      if self.pos.x < self.player.pos.x:
        # self.status = 'Right_Run'
        self.direction.x = 1
      elif self.pos.x > self.player.pos.x:
        # self.status = 'Left_Run'
        self.direction.x = -1
    self.pos.x += self.direction.x * self.speed * dt
    self.collision_rect.centerx = round(self.pos.x)
    self.rect.x = round(self.pos.x)

    # get horizontal collisions
    # self.collision('horizontal')

    # Vertical movement + collision
    # gravity
    self.direction.y += self.gravity
    self.pos.y += self.direction.y * dt
    self.collision_rect.centery = round(self.pos.y)
    self.rect.y = round(self.pos.y)

    # get vertical collisions
    self.collision('vertical')
    # self.moving_floor = None

  def update(self, dt, camera_left_x):
    self.prev_rect = self.rect.copy()
    self.get_status()
    self.move(dt)
    # self.check_floor_contact()
    self.animate(dt)