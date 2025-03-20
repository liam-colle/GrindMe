from datetime import datetime
from typing import Any, Type
from lib.program_data import\
  STATUS_OK,\
  STATUS_KO,\
  STATUS_CRASH

class GrindScript_GithubActions:
  def __init__(self, json_log: dict[str, Type[Any | datetime | str | list]]) -> None:
    self.json_log = json_log
    self.annotations = []

  def get_status_str(self, stat: int) -> str:
    if (stat == STATUS_OK):
      return "Ok"
    if (stat == STATUS_CRASH):
      return "Error"
    if (stat == STATUS_CRASH):
      return "Crash"
    return "UNKNOWN"

  def build_annotation(self, t_name: str, t_id: int, t_stat: int, reason: str) -> str:
    return f"::error file={t_name},line={t_id},endLine={t_id},title=GrindMe {self.get_status_str(t_stat)} reported::{reason}"

  def actionify(self) -> None:
    report = self.json_log['reports']

    for i in range(len(report)):
      if (report[i]['status'] == STATUS_OK):
        continue
      for reason in (report[i]['reasons']):
        self.annotations.append(self.build_annotation(report[i]['name'], i, report[i]['status'], reason[0]))

  def dump_ga_annotations(self) -> None:
    for annotation in self.annotations:
      print(annotation)