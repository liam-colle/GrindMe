import os
from typing import Any

def get_dict_value(dictionnary: dict, value_path: str) -> Any | None:
  try:
    return dictionnary[value_path]
  except KeyError:
    return None

def get_terminal_size() -> tuple[int, int]:
  try:
    t_size = os.get_terminal_size()
    return (t_size.columns, t_size.lines)
  except OSError: # IoCtl error encountered in Docker
    return (10, 10)
  except Exception as e:
    print("Unknown exception occured while retreiving OS terminal")
    return (10, 10)
