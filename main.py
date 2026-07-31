import pygame 
from scripts.settings import *
from pytmx.util_pygame import load_pygame
from scripts.sprites import Sprite

class Game:
  def __init__(self):
    pygame.init()
    self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pokemon Game")
    
    self.all_sprites = pygame.sprite.Group() 
    
    
    
    
    self.import_assets()
    self.setup(self.tmx_maps['world'], 'house') 
    
    
  def import_assets(self):
    self.tmx_maps = {
      'world': load_pygame('assets/data/maps/world.tmx'),  
      
      }
     
  def setup(self, tmx_map, player_start_pos):
    for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles():
      Sprite(
        pos=(x*TILE_SIZE, y*TILE_SIZE), 
        surf=surf,
        groups=self.all_sprites) 
      
      
  def run(self):
    while True:
      
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          exit() 
          
      self.all_sprites.draw(self.display_surface) 
      pygame.display.flip()
      

game = Game()

if __name__ == '__main__':
  game.run() 
    

