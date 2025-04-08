import json, os
from sys import stderr
from io import TextIOWrapper
from lib.exit_codes import EXIT_FAIL
from lib.exceptions import gs_excepts_panicstr
from lib.program_data import\
  DEF_SCRIPT_NAME,\
  DEF_SCRIPT_PATH,\
  DEF_SCRIPT_INDENT,\
  EXAMPLE_SCRIPT


class GrindScript_ScriptGenerator:
  def __init__(self) -> None:
    try:
      ## Prompts
      self.pr_outpath: str = input(f"Path to grindme directory [Default: {DEF_SCRIPT_PATH}]: ") or DEF_SCRIPT_PATH
      self.pr_outname: str = input(f"Name of script file [Default: {DEF_SCRIPT_NAME}]: ") or DEF_SCRIPT_NAME
      try:
        self.pr_indents: int = int(input(f"Number of indents [Default: {DEF_SCRIPT_INDENT}]: ") or DEF_SCRIPT_INDENT)
      except ValueError:
        print(f"Wrong value inserted! Defaulting to: {DEF_SCRIPT_INDENT}")
        self.pr_indents: int = DEF_SCRIPT_INDENT
      self.out_file: TextIOWrapper = None

      if (not os.path.exists(self.pr_outpath)):
        os.makedirs(self.pr_outpath)
      self.script = EXAMPLE_SCRIPT
      self.out_file = open(f"{self.pr_outpath}/{self.pr_outname}", "w")
    except FileNotFoundError:
      message = f"GrindScript file \"{self.pr_outpath}/{self.pr_outname}\" not found"
      print(gs_excepts_panicstr(message), file = stderr)
      exit(EXIT_FAIL)
    except Exception as e:
      message = f"An unknown exception occured:\n{e}"
      print(gs_excepts_panicstr(message), file = stderr)
      exit(EXIT_FAIL)

  def write(self):
    try:
      self.out_file.write(json.dumps(self.script, indent = self.pr_indents))
    except Exception as e:
      message = f"An unknown exception occured:\n{e}"
      print(gs_excepts_panicstr(message), file = stderr)
      exit(EXIT_FAIL)

  def __del__(self):
    if (self.out_file):
      self.out_file.close()
