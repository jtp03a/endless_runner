import pygame
from state.level.spritesheet import SpriteSheet
from state.level.settings import *
from os import walk
from pygame.math import Vector2 as vector
from state.level.entity import Entity

class Enemy(Entity):
  def __init__(self, pos, groups, collision_sprites, player, path):
    super().__init__(pos, groups, path)
    self.player = player
    if pos[0] > self.player.pos.x:
      # self.anim_dict['Idle'] = [pygame.transform.flip(image, True, False) for image in self.anim_dict['Idle']]
      # self.anim_dict['Run'] = [pygame.transform.flip(image, True, False) for image in self.anim_dict['Run']]
      # self.anim_dict['Attack'] = [pygame.transform.flip(image, True, False) for image in self.anim_dict['Attack']]
      # self.anim_dict['Death'] = [pygame.transform.flip(image, True, False) for image in self.anim_dict['Death']]
      self.status = 'Left_Idle'
    else:
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
    self.on_floor = False
    self.is_player = False
    self.dead = False
    self.dying = False
  
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
        x_pos = self.rect.bottomleft[0] + 44
        self.rect = current_animation[int(self.frame_index)].get_rect(bottomright = (x_pos, self.rect.bottomleft[1]))

      self.frame_index += 7 * dt 

      if self.frame_index >= len(current_animation) and not self.dead:
        self.frame_index = 0
        if self.dying:
          self.dead = True
          self.direction.x = 0

      if self.dead:
        self.frame_index = len(current_animation) -1

      self.image = current_animation[int(self.frame_index)]

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
    if not self.dying and self.on_floor:
      if self.pos.x > self.player.pos.x and self.pos.x - self.player.pos.x > 60:
        # if self.status.split('_')[0] == 'Right':
        #   self.anim_dict['Run'] = [pygame.transform.flip(image, True, False) for image in self.anim_dict['Run']]
        #   self.anim_dict['Idle'] = [pygame.transform.flip(image, True, False) for image in self.anim_dict['Idle']]
        #   self.anim_dict['Attack'] = [pygame.transform.flip(image, True, False) for image in self.anim_dict['Attack']]
        #   self.anim_dict['Death'] = [pygame.transform.flip(image, True, False) for image in self.anim_dict['Death']]
        self.direction.x = -.25
        self.status = 'Left_Run'
      elif self.pos.x < self.player.pos.x and self.player.pos.x - self.pos.x > 60:
        # if self.status.split('_')[0] == 'Left':
        #   self.anim_dict['Run'] = [pygame.transform.flip(image, True, False) for image in self.anim_dict['Run']]
        #   self.anim_dict['Idle'] = [pygame.transform.flip(image, True, False) for image in self.anim_dict['Idle']]
        #   self.anim_dict['Attack'] = [pygame.transform.flip(image, True, False) for image in self.anim_dict['Attack']]
        #   self.anim_dict['Death'] = [pygame.transform.flip(image, True, False) for image in self.anim_dict['Death']]
        self.direction.x = .25
        self.status = 'Right_Run'
      else:
        self.direction.x = 0
        self.attacking = True
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
    self.animate(dt)