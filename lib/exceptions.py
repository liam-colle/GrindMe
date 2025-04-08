from colorama import Fore

def gs_excepts_failstr(message: str) -> str:
  return\
    f"[GrindMe] - {Fore.RED}FAIL!{Fore.RESET}\n" +\
    f"> {Fore.YELLOW}{message}{Fore.RESET}\n"

def gs_excepts_panicstr(message: str) -> str:
  return\
    f"[GrindMe] - {Fore.RED}PANIC!{Fore.RESET}\n" +\
    f"> {Fore.YELLOW}{message}{Fore.RESET}"

class GS_ExecutionError(Exception):
  """Sent in case the program fails"""
  def __init__(self, message: str):
    self.message = message
    super().__init__(self.message)

  def __str__(self):
    return f"{self.message}"

class GSP_CouldNotLoadJSON(Exception):
  """Sent in case the parser cannot load the json file (E.g.: File does not exist)"""
  def __init__(self, message: str):
    self.message = message
    super().__init__(self.message)

  def __str__(self):
      return gs_excepts_failstr(self.message)

class GSP_JSONParseError(Exception):
  """Sent in case the json file is malformed (E.g.: json lib cannot parse it)"""
  def __init__(self, message: str):
    self.message = message
    super().__init__(self.message)

  def __str__(self):
    return f"{self.message}"

class GSE_ValgrindFail(Exception):
  """Sent in case the executor fails"""
  def __init__(self, message: str):
    self.message = message
    super().__init__(self.message)

  def __str__(self):
    return f"{self.message}"

class GSE_ExecutionError(Exception):
  """Sent in case the executor fails"""
  def __init__(self, message: str):
    self.message = message
    super().__init__(self.message)

  def __str__(self):
    return f"{self.message}"
