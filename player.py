import pygame
from spritesheet import SpriteSheet
from settings import *
from os import walk
from pygame.math import Vector2 as vector

class Player(pygame.sprite.Sprite):
  def __init__(self, pos, groups, collision_sprites):
    super().__init__(groups)
    self.import_assets('./graphics/player')
    self.status = 'Left_Idle'
    self.frame_index = 0
    self.image = self.anim_dict[self.status][self.frame_index]
    self.rect = self.image.get_rect(center = pos)
    self.z = LAYERS['Ground']
    self.left_border = 0
    self.right_border = 1280

    # float based movement
    self.pos = vector(self.rect.center)
    self.direction = vector(0, 0)
    self.speed = 400

    self.attacking = False

    self.collision_sprites = collision_sprites
    self.collision_rect = self.rect.inflate(self.rect.width, self.rect.height * .75)
    self.prev_rect = self.rect.copy()

    self.gravity = 15
    self.jump_speed = 500
    self.on_floor = True

  def import_assets(self, path):
    self.anim_dict = {}
    for index, folder in enumerate(walk(path)):
      for file in folder[2]:
        file_name = file.split('.')[0]
        self.anim_dict[file_name] = []
        num_frames = START_POS[file_name][2]
        start_x = START_POS[file_name][0]
        start_y = START_POS[file_name][1]
        rect_w = START_POS[file_name][3]
        rect_h = START_POS[file_name][4]
        self.spritesheet = SpriteSheet(f'./graphics/player/{file}')
        for _ in range(num_frames):
          new_image = self.spritesheet.image_at((start_x, start_y, rect_w, rect_h), colorkey=(255, 255, 255))
          self.anim_dict[file_name].append(new_image)
          start_x += 200
  
  def get_status(self):
    # idle
    if self.direction.x == 0:
      self.status = self.status.split('_')[0] + '_Idle'

    # attacking
    if self.attacking:
      self.status = self.status.split('_')[0] + '_Attack'

    # jumping
    # if self.direction.y != 0 and not self.on_floor:
    #   self.status = self.status.split('_')[0] + '_jump'

    # # ducking
    # if self.ducking and self.on_floor:
    #   self.status = self.status.split('_')[0] + '_duck'

  def animate(self, dt):
    current_animation = self.anim_dict[self.status]

    self.frame_index += 10 * dt
    
    if self.frame_index >= len(current_animation):
      self.frame_index = 0
      if self.attacking:
        self.attacking = False

    self.image = current_animation[int(self.frame_index)]

  def input(self, camera_left_x):
    keys =  pygame.key.get_pressed()
    # movement keys
    if keys[pygame.K_LEFT] and self.pos.x > camera_left_x + 5:
        self.direction.x = -1
        self.status = 'Left'
    elif keys[pygame.K_RIGHT]:
        self.direction.x = 1
        self.status = 'Right'
    else:
        self.direction.x = 0
    
    if keys[pygame.K_UP] and self.on_floor:
      self.direction.y = -self.jump_speed

    if pygame.mouse.get_pressed()[0]:
      self.frame_index = 0
      self.attacking = True

    # if keys[pygame.K_UP] and self.on_floor:
    #   self.direction.y = -self.jump_speed

    # if keys[pygame.K_DOWN]:
    #   self.ducking = True
    # else:
    #   self.ducking = False

    # if keys[pygame.K_SPACE] and self.can_shoot:

    #   bullet_direction = vector(1,0) if self.status.split('_')[0] == 'right' else vector(-1,0)
    #   pos = self.rect.center + bullet_direction * 60
    #   y_offset = vector(0, -16) if not self.ducking else vector(0, 10)
    #   self.shoot(pos + y_offset, bullet_direction, self)

    #   self.can_shoot = False
    #   self.shot_time = pygame.time.get_ticks()

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
          if self.collision_rect.bottom >= sprite.mask_rect.top:
            self.collision_rect.bottom = sprite.mask_rect.top
            self.on_floor = True
            self.direction.y = 0
          self.pos.y = self.rect.y

     # check if the player is falling
    if self.on_floor and self.direction.y != 0:
      self.on_floor = False
      

  def move(self, dt, camera_left_x):  
    # Horizontal movement + collision
    self.pos.x += self.direction.x * self.speed * dt
    self.collision_rect.centerx = round(self.pos.x)
    self.rect.x = round(self.pos.x)
    if self.rect.x < camera_left_x:
      self.rect.x = camera_left_x

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
    self.input(camera_left_x)
    self.get_status()
    self.move(dt, camera_left_x)
    # self.check_floor_contact()
    self.animate(dt)