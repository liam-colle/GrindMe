import os
from sys import stderr
from typing import Any, TypeVar

T = TypeVar("T")
def get_dict_value(dictionnary: dict, value_path: list[str], default: T = None) -> T | Any | None:
  try:
    for key in value_path:
      dictionnary = dictionnary[key]
    return dictionnary
  except KeyError:
    return default

def get_terminal_size() -> tuple[int, int]:
  try:
    t_size = os.get_terminal_size()
    return (t_size.columns, t_size.lines)
  except OSError: # IoCtl error encountered in Docker
    return (10, 10)
  except Exception as e:
    print("Unknown exception occured while retreiving OS terminal", file = stderr)
    return (10, 10)
