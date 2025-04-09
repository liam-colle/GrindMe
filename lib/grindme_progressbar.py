import os
from math import floor
from lib.utils import get_terminal_size
from colorama import Fore

PB_ST_BRAKCET = "["
PB_VAL_PROG = "="
PB_INVAL_PROG = " "
PB_END_BRAKCET = "]"

class Grindme_ProgressBar:
  def __init__(self):
    self.__length: int = get_terminal_size()[0] // 4
    self.progress: int = 0

  def pb_print(self, add_color: True = True):
    valid_progress: int = floor((self.progress / 100) * self.__length)
    inval_progress: int = self.__length - valid_progress
    color = Fore.RED
    if (self.progress >= 25 and self.progress < 75):
      color = Fore.YELLOW
    if (self.progress >= 75):
      color = Fore.GREEN
    if (add_color == True):
      print(color, end = "")
    print(PB_ST_BRAKCET, end = "")
    print(PB_VAL_PROG * valid_progress, end = "")
    print(PB_INVAL_PROG * inval_progress, end = "")
    print(PB_END_BRAKCET, end = "")
    if (add_color == True):
      print(f"{Fore.RESET} - {color}{self.progress}%{Fore.RESET}")
    else:
      print(f" - {self.progress}%")
