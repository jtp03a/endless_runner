import pygame
from pygame.math import Vector2 as vector
from state.level.settings import *
from abc import ABC, abstractmethod

class Camera:
  def __init__(self, player):
    self.player = player
    self.offset = vector(0, 0)
    self.offset_float = vector(0, 0)
    self.CONST = vector(-WINDOW_WIDTH / 2 + player.rect.w, -WINDOW_HEIGHT /2)

    # camera box setup
    self.camera_borders = {'left': 0, 'right': 200, 'top': 100, 'bottom': 100}
    l = self.camera_borders['left']
    t = self.camera_borders['top']
    w = WINDOW_WIDTH - self.camera_borders['left'] - self.camera_borders['right']
    h = WINDOW_HEIGHT - self.camera_borders['top'] - self.camera_borders['bottom']
    self.camera_rect = pygame.Rect(l, t, w, h)

  def setmethod(self, method):
    self.method = method

  def scroll(self):
    self.method.scroll()

class CamScroll(ABC):
  def __init__(self, camera, player):
    self.camera = camera
    self.player = player

  @abstractmethod
  def scroll(self):
    pass

class Follow(CamScroll):
  def __init__(self, camera, player):
    super().__init__(camera, player)

  def scroll(self):
    self.camera.offset_float.x += (self.player.rect.x - self.camera.offset_float.x + self.camera.CONST.x)
    self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y)
    self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)

class Box(CamScroll):
  def __init__(self, camera, player):
    super().__init__(camera, player)

  def scroll(self):
    if self.player.rect.left < self.camera.camera_rect.left:
      self.camera.camera_rect.left = self.player.rect.left
    if self.player.rect.right > self.camera.camera_rect.right:
      self.camera.camera_rect.right = self.player.rect.right

    self.camera.offset_float.x = self.camera.camera_rect.left - self.camera.camera_borders['left']
    self.camera.offset_float.y = self.camera.camera_rect.top - self.camera.camera_borders['top']

    # self.camera.offset_float.x += (self.player.rect.x - self.camera.offset_float.x + self.camera.CONST.x)
    # self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y)
    self.camera.offset.x = int(self.camera.offset_float.x)
    self.camera.offset.y = int(self.camera.offset_float.y)

    

class Border(CamScroll):
  def __init__(self, camera, player):
    super().__init__(camera, player)

  def scroll(self):
    self.camera.offset_float.x += (self.player.rect.x - self.camera.offset_float.x + self.camera.CONST.x)
    self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y)
    self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)
    self.camera.offset.x = max(self.player.left_border, self.camera.offset.x)
    self.camera.offset.x = min(self.camera.offset.x, self.player.right_border - WINDOW_WIDTH)


class Auto(CamScroll):
  def __init__(self, camera, player):
    super().__init__(camera, player)

  def scroll(self):
    self.camera.offset.x += 1