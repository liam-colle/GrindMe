import json, os
from enum import Enum
from datetime import datetime
from typing import Type, Any
from sys import stderr
from io import TextIOWrapper
from lib.exit_codes import EXIT_FAIL
from lib.exceptions import gs_excepts_panicstr, gs_excepts_failstr
from lib.program_data import\
  DEF_REPORT_PREFIX,\
  DEF_REPORT_PATH,\
  DEF_REPORT_INDENT,\
  EXAMPLE_SCRIPT

class GrindScript_DumperTypes(Enum):
  UNKNOWN_DUMPER = -1
  JSON_DUMPER = 0

def gs_identify_dump(type: str | None) -> GrindScript_DumperTypes:
  if (type == None):
    return GrindScript_DumperTypes.JSON_DUMPER
  match type.lower():
    case "json":
      return GrindScript_DumperTypes.JSON_DUMPER
    case _:
      return GrindScript_DumperTypes.UNKNOWN_DUMPER

class Dumper:
  def __init__(self, json_log: dict[str, Type[Any | datetime | str | list]],
               file: TextIOWrapper, write_data: dict[Any]) -> None:
    self.json_log: dict[str, Type[Any | datetime | str | list]] = json_log
    self.output_data: Any = None
    self.write_data: dict[Any] = write_data
    self.file: TextIOWrapper = file

  def convert(self) -> None:
    self.output_data = self.output_data

  def write(self) -> None:
    self.file.write(self.output_data)

class GrindScript_ReportDumper:
  class GrindScript_ReportJSONDumper(Dumper):

    def __init__(self, json_log, file, write_data) -> None:
      super().__init__(json_log, file, write_data)
      self.output_data: dict[str, Type[Any | datetime | str | list]] = None

    def convert(self):
      self.output_data = self.json_log

    def write(self) -> None:
      self.file.write(json.dumps(self.output_data, indent = self.write_data['indents']))

  DUMPER_TYPES = GrindScript_DumperTypes

  def __init__(self, json_log: dict[str, Type[Any | datetime | str | list]],
               path: str, type: GrindScript_DumperTypes) -> None:
    self.dumper_type = type
    self.json_log = json_log
    self.pr_fullpath: str = ""
    self.pr_outpath: str = path or DEF_REPORT_PATH
    self.pr_outname: str = DEF_REPORT_PREFIX + "unknown" + ".json"
    self.out_file: TextIOWrapper = None

    if (type == self.DUMPER_TYPES.UNKNOWN_DUMPER):
      message = f"Incorrect dumper type"
      print(gs_excepts_failstr(message), file = stderr)
      exit(EXIT_FAIL)
    try:
      self.pr_outname = path or DEF_REPORT_PREFIX + str(json_log['exec_epoch']) + ".json"
    except Exception as e:
      message = f"An unknown exception occured:\n{e}"
      print(gs_excepts_panicstr(message), file = stderr)
      exit(EXIT_FAIL)
    self.pr_fullpath = path or self.pr_outpath + self.pr_outname
    try:
      if (not os.path.exists(self.pr_outpath)):
        os.makedirs(self.pr_outpath)
      self.script = EXAMPLE_SCRIPT
      self.out_file = open(f"{self.pr_outpath}/{self.pr_outname}", "w")
    except FileNotFoundError:
      message = f"GrindScript file \"{self.pr_outpath}/{self.pr_outname}\" not found"
      print(gs_excepts_failstr(message), file = stderr)
      exit(EXIT_FAIL)
    except Exception as e:
      message = f"An unknown exception occured:\n{e}"
      print(gs_excepts_panicstr(message), file = stderr)
      exit(EXIT_FAIL)

  def create_dumper(self) -> Dumper:
    match (self.dumper_type):
      case self.DUMPER_TYPES.JSON_DUMPER:
        write_data: dict = {
          'indents': DEF_REPORT_INDENT
        }
        return self.GrindScript_ReportJSONDumper(self.json_log, self.out_file,
                                                 write_data)
      case _:
        message = f"Incorrect dumper type"
        print(gs_excepts_failstr(message), file = stderr)
        exit(EXIT_FAIL)


  def write(self):
    try:
      dumper = self.create_dumper()
      dumper.convert()
      dumper.write()
    except Exception as e:
      message = f"An unknown exception occured:\n{e}"
      print(gs_excepts_panicstr(message), file = stderr)
      exit(EXIT_FAIL)

  def __del__(self):
    if (self.out_file):
      self.out_file.close()
