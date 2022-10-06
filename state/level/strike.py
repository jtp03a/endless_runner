import pygame

class Strike(pygame.sprite.Sprite):
  def __init__(self, animation, player, groups):
    super().__init__(groups)
    self.animation = animation
    self.player = player
    self.frame_index = 0
    self.image = pygame.Surface((0, 0))
    self.rect = self.image.get_rect(topleft = player.rect.topleft)
    self.is_player = True
    self.dying = None
    self.z = 2
    self.direction = 0

  def update(self, dt, camera_left_x):
    self.mask = pygame.mask.from_surface(self.image)






