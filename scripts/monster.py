from scripts.settings import *
from scripts.game_data import MONSTER_DATA
from random import randint, choice, random


class Monster:
  def __init__(self, name, level):
    self.name = name
    self.level = level
    
    self.element = MONSTER_DATA[name]['stats']['element'] 
    self.base_stats = MONSTER_DATA[name]['stats'] 
    
    self.xp = randint(0, 1000) 
    self.level_up = self.level * 150 
