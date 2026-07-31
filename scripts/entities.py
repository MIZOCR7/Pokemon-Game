from scripts.settings import *

class Player(pygame.sprite.Sprite):
  def __init__(self, pos, groups):
    super().__init__(groups)
    
    self.image = pygame.Surface((100,100)) 
    self.image.fill('red')
    self.rect = self.image.get_frect(topleft = pos)
    
    self.direction = Vector()   
    self.speed = 250
  
  def input(self):
    keys = pygame.key.get_pressed()
    input_vector = Vector() 
    up = keys[pygame.K_w]
    down = keys[pygame.K_s]
    left = keys[pygame.K_a]
    right = keys[pygame.K_d]
    
    if up:
      input_vector.y -= 1
    if down:
      input_vector.y += 1
    if right:
      input_vector.x += 1
    if left:
      input_vector.x -= 1 
    
    if input_vector.magnitude() != 0:
      input_vector = input_vector.normalize() 
    
    self.direction = input_vector 
    
  def move(self, dt):
    self.rect.center += self.direction * self.speed * dt 

  def update(self, dt):
    self.input() 
    self.move(dt) 
