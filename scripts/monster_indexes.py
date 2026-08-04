from scripts.settings import *
from scripts.support import draw_bar

class MonsterIndex:
  def __init__(self, monsters, fonts, monster_frames): 
    self.display_surface = pygame.display.get_surface() 
    self.fonts = fonts 
    self.monsters = monsters
    self.frame_index = 0 
    
    self.tint_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    self.tint_surf.set_alpha(200) 
    
    self.icon_frames = monster_frames['icons']
    self.monster_frames = monster_frames['monsters'] 
    
    self.index = 0
    
    self.main_rect = pygame.FRect(0, 0, WINDOW_WIDTH * 0.6, WINDOW_HEIGHT * 0.8).move_to(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)) 
    
    self.visible_items = 6
    self.list_width = self.main_rect.width *  0.3 
    self.item_height = self.main_rect.height / self.visible_items 
    self.selected_index = None 
  
  def input(self):
    keys = pygame.key.get_just_pressed() 
    if keys[pygame.K_w]:
      self.index -= 1
    if keys[pygame.K_s]: 
      self.index += 1 
    if keys[pygame.K_SPACE]:
      if self.selected_index is not None:
        selected_monster = self.monsters[self.selected_index] 
        current_monster = self.monsters[self.index]
        self.monsters[self.index] = selected_monster 
        self.monsters[self.selected_index] = current_monster 
        self.selected_index = None
      else: 
        self.selected_index = self.index
        
        
    self.index = self.index % len(self.monsters) 
    
  
  def display_list(self):
    v_offset = 0 if self.index < self.visible_items else -(self.index - self.visible_items + 1) * self.item_height 
    for index, monster in self.monsters.items():
      
      bg_color =  COLORS['gray'] if self.index != index else COLORS['light'] 
      text_color = COLORS['white'] if self.selected_index != index else COLORS['gold'] 
      
      top = self.main_rect.top + index * self.item_height + v_offset 
      item_rect = pygame.FRect(self.main_rect.left, top, self.list_width, self.item_height)
      
      text_surf = self.fonts['regular'].render(monster.name , False, text_color) 
      text_rect = text_surf.get_frect(midleft = item_rect.midleft + Vector(90, 0))  
      
      icon_surf = self.icon_frames[monster.name]
      icon_rect = icon_surf.get_frect(center=item_rect.midleft + Vector(45, 0)) 
      
      if item_rect.colliderect(self.main_rect):
        
        if item_rect.collidepoint(self.main_rect.topleft):
          pygame.draw.rect(self.display_surface, bg_color, item_rect, 0, 0, 12) 
        elif item_rect.collidepoint(self.main_rect.bottomleft + Vector(1, -1)):
          pygame.draw.rect(self.display_surface, bg_color, item_rect, 0,0,0,0,12,0) 
        else: 
          pygame.draw.rect(self.display_surface, bg_color, item_rect)
           
        self.display_surface.blit(text_surf, text_rect) 
        self.display_surface.blit(icon_surf, icon_rect) 
    
    for i in range(min(self.visible_items, len(self.monsters))):
      y = self.main_rect.top + self.item_height * i
      left = self.main_rect.left
      right = self.main_rect.left + self.list_width 
      pygame.draw.line(self.display_surface, COLORS['light'], (left,y), (right, y)) 
    
    shadow_surf = pygame.Surface((4, self.main_rect.height)) 
    shadow_surf.set_alpha(100) 
    self.display_surface.blit(shadow_surf, (self.main_rect.left + self.list_width - 4, self.main_rect.top)) 
  
  
  def display_main(self, dt):
    
    monster = self.monsters[self.index] 
    
    rect = pygame.FRect(self.main_rect.left + self.list_width, self.main_rect.top, self.main_rect.width - self.list_width, self.main_rect.height) 
    pygame.draw.rect(self.display_surface, COLORS['dark'], rect, 0,12,0,12,0) 
    
    top_rect = pygame.FRect(rect.topleft, (rect.width, rect.height * 0.4))
    pygame.draw.rect(self.display_surface, COLORS[monster.element], top_rect, 0,0,0,12) 
    
    self.frame_index += ANIMATION_SPEED * dt 
    monster_surf = self.monster_frames[monster.name]['idle'][int(self.frame_index) % len(self.monster_frames[monster.name]['idle'])]    
    monster_rect = monster_surf.get_frect(center=top_rect.center) 
    self.display_surface.blit(monster_surf, monster_rect) 
    
    
    name_surf = self.fonts['bold'].render(monster.name, False, COLORS['white']) 
    name_rect = name_surf.get_frect(topleft=top_rect.topleft + Vector(10,10)) 
    self.display_surface.blit(name_surf, name_rect) 
    
    level_surf = self.fonts['regular'].render(f"Lvl: {monster.level}", False, COLORS['white'])
    level_rect = level_surf.get_frect(bottomleft=top_rect.bottomleft + Vector(10,-16)) 
    self.display_surface.blit(level_surf, level_rect) 
    draw_bar(
      surface=self.display_surface,
      rect = pygame.FRect(level_rect.bottomleft, (100,4)), 
      value=monster.xp,
      max_value=monster.level_up,
      color=COLORS['white'],
      bg_color=COLORS['dark'],
      radius=1,
    )
    
    element_surf = self.fonts['regular'].render(monster.element, False, COLORS['white']) 
    element_rect = element_surf.get_frect(bottomright=top_rect.bottomright + Vector(-10,-10)) 
    self.display_surface.blit(element_surf, element_rect) 
    
    
    bar_data = {
      'width': rect.width * 0.45,
      'height': 30,
      'top': top_rect.bottom + 50,
      'left_side': rect.left + rect.width / 4,
      
    }
    
    
    
  def update(self, dt):
    self.input() 
    
    self.display_surface.blit(self.tint_surf, (0,0)) 
     
    self.display_list() 
    self.display_main(dt) 
