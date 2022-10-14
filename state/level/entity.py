import pygame
from os import walk
from state.level.spritesheet import SpriteSheet
from pygame.math import Vector2 as vector
from state.level.settings import *

class Entity(pygame.sprite.Sprite):
  def __init__(self, pos, groups, path):
    super().__init__(groups)
    self.asset_type = path
    self.import_assets(f'./state/level/graphics/{path}')

    self.on_floor = True
    

  def import_assets(self, path):
    self.anim_dict = {}
    for index, folder in enumerate(walk(path)):
      for file in folder[2]:
        file_name = file.split('.')[0]
        num_frames = sprite_POS[self.asset_type][file_name][2]
        start_y = sprite_POS[self.asset_type][file_name][1]
        rect_w = sprite_POS[self.asset_type][file_name][3]
        rect_h = sprite_POS[self.asset_type][file_name][4]
        self.spritesheet = SpriteSheet(f'{path}/{file}')
        self.anim_dict[f'Right_{file_name}'] = []
        self.anim_dict[f'Left_{file_name}'] = []
        start_x = sprite_POS[self.asset_type][file_name][0]
        for _ in range(num_frames):
          new_image = self.spritesheet.image_at((start_x, start_y, rect_w, rect_h), colorkey=(255, 255, 255))
          self.anim_dict[f'Right_{file_name}'].append(new_image)
          start_x += 200
        start_x = sprite_POS[self.asset_type][file_name][0]
        for _ in range(num_frames):
          new_image = self.spritesheet.image_at((start_x, start_y, rect_w, rect_h), colorkey=(255, 255, 255))
          fliped_image = pygame.transform.flip(new_image, True, False)
          self.anim_dict[f'Left_{file_name}'].append(fliped_image)
          start_x += 200