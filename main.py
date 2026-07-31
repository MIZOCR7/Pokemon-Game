import pygame 
from scripts.settings import *
from pytmx.util_pygame import load_pygame
from scripts.sprites import Sprite, AnimatedSprite
from scripts.entities import Player
from scripts.groups import AllSprites 
from scripts.support import *

class Game:
  def __init__(self):
    pygame.init()
    self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pokemon Game")
    self.clock = pygame.time.Clock() 
    
    self.all_sprites = AllSprites()
    
    
    
    
    self.import_assets()
    self.setup(self.tmx_maps['world'], 'house') 
    
    
  def import_assets(self):
    self.tmx_maps = {
      'world': load_pygame('assets/data/maps/world.tmx'),  
      'hospital': load_pygame('assets/data/maps/hospital.tmx') 
      
      }
    self.overworld_frames = {
      'water': import_folder('assets', 'graphics', 'tilesets', 'water'),
      
    }
     
     
  def setup(self, tmx_map, player_start_pos):
    
    for layer in ['Terrain', 'Terrain Top']:
    
      for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), surf, self.all_sprites)
    
    
    
    for obj in tmx_map.get_layer_by_name('Objects'):
      Sprite((obj.x, obj.y), obj.image, self.all_sprites) 
    
    
    for obj in tmx_map.get_layer_by_name('Entities'):
      if obj.name == 'Player' and obj.properties['pos'] == player_start_pos:
        self.player = Player((obj.x, obj.y), self.all_sprites) 
    
    for obj in tmx_map.get_layer_by_name('Water'):
      for x in range(int(obj.x), int(obj.x + obj.width), TILE_SIZE):
        for y in range(int(obj.y), int(obj.y + obj.height), TILE_SIZE):
          AnimatedSprite((x,y), self.overworld_frames['water'], self.all_sprites) 
    
      
  def run(self):
    while True:
      dt = self.clock.tick() / 1000  
      
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          exit() 
      
      
      self.all_sprites.update(dt) 
      self.display_surface.fill('black') 
      self.all_sprites.draw(self.player.rect.center)  
      pygame.display.update()
      

game = Game()

if __name__ == '__main__':
  game.run() 
    

