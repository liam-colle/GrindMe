from typing import Any

def get_dict_value(dictionnary: dict, value_path: str) -> Any | None:
  try:
    return dictionnary[value_path]
  except KeyError:
    return None
