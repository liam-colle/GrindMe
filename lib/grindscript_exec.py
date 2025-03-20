import subprocess, os, re
from lib.grindscript_parse import GrindScript_Parser
from lib.grindme_progressbar import Grindme_ProgressBar
from random import randint
from typing import Type, Any
from colorama import Fore, Back
from datetime import datetime
from math import floor
from lib.exceptions import\
  gs_excepts_failstr
from lib.exit_codes import\
  EXIT_FAIL
from lib.program_data import\
  STATUS_OK,\
  STATUS_KO,\
  STATUS_CRASH,\
  SEV_INFO,\
  SEV_MINOR,\
  SEV_MAJOR,\
  SEV_CRITICAL,\
  VALGRIND_ERRORS,\
  VALGRIND_MEMLEAK


class GrindScript_Executer:
  class GrindScript_Valgrinder:
    class GrindScript_ErrCheck:
      def __init__(self, out_data: str):
        self.out_data: str = out_data
        self.report: list[tuple[str, int]] = []
        self.status: int = STATUS_OK

      def parse(self) -> None:
        if (self.out_data == None):
          return None
        for error in VALGRIND_ERRORS:
          occurences = re.findall(error[0], self.out_data, re.MULTILINE)
          if (len(occurences) > 0):
            self.report.append((error[1], error[2]))
            if (self.status == STATUS_OK):
              self.status = STATUS_KO
            if (self.status == STATUS_KO and error[2] == SEV_CRITICAL):
              self.status = STATUS_CRASH
        if self.out_data.find("in use at exit: 0 bytes in 0 blocks") == -1:
          self.report.append(VALGRIND_MEMLEAK)
          if (self.status == STATUS_OK):
            self.status = STATUS_KO

    def __init__(self, test: str, program_name: str, program_args: list[str]):
      self.test: str = test
      self.program_name: str = program_name
      self.program_args: list[str] = program_args
      self.exit_code: int = 0
      self.output: str = ""
      self.outpath = f"/tmp/grindme/{os.getpid()}"
      self.outfilename = f"{self.test}"
      self.filename_rev = 0
      self.errors: list[str, int]

    def read_output(self) -> str | None:
      try:
        outfile = open(f"{self.outpath}/{self.outfilename}_{self.filename_rev}.log", "r")
        data = outfile.read()
        outfile.close()
        return data
      except:
        return None

    def exec(self) -> GrindScript_ErrCheck:
      try:
        if (not os.path.exists(self.outpath)):
          os.makedirs(self.outpath)
        outfile = open(f"{self.outpath}/{self.outfilename}_{self.filename_rev}.log", "x")
      except FileExistsError:
        self.filename_rev += 1
        return self.exec()
      except FileNotFoundError:
        message = f"Execution failure in Test '{self.test}'"
        print(gs_excepts_failstr(message))
        exit(EXIT_FAIL)
      try:
        self.output = subprocess.check_output(['valgrind', f'--log-file={self.outpath}/{self.outfilename}_{self.filename_rev}.log', self.program_name]
                                              + self.program_args, stderr = outfile)
      except subprocess.CalledProcessError as e:
        self.exit_code = e.returncode
      except:
        message = f"Execution failure in Test '{self.test}'"
        print(gs_excepts_failstr(message))
        exit(EXIT_FAIL)
      err_check = self.GrindScript_ErrCheck(self.read_output())
      err_check.parse()
      return err_check

  class GrindScript_TestResults:
    def __init__(self, name: str, status: int, reasons: list[str, int]):
      self.name = name
      self.status_int = status
      if (status <= STATUS_OK):
        self.status = f"{Fore.GREEN}OK{Fore.RESET}"
      if (status == STATUS_KO):
        self.status = f"{Fore.RED}KO{Fore.RESET}"
      if (status == STATUS_CRASH):
        self.status = f"{Back.RED + Fore.BLACK}CRASH{Back.RESET + Fore.RESET}"
      self.reasons: list[str, int] = reasons

    def get_fail_severity_emoji(self, severity: int) -> str:
      if (severity == SEV_MINOR):
        return "⚠️"
      if (severity == SEV_MAJOR):
        return "⚠️"
      if (severity == SEV_CRITICAL):
        return "⚠️"
      return "ℹ️"

    def get_fail_severity_color(self, severity: int) -> str:
      if (severity == SEV_INFO):
        return Fore.LIGHTWHITE_EX
      if (severity == SEV_MINOR):
        return Fore.YELLOW
      if (severity == SEV_MAJOR):
        return Fore.RED
      if (severity == SEV_CRITICAL):
        return Back.RED + Fore.BLACK
      return Fore.WHITE

    def print(self) -> None:
      print(f"== TEST RESULTS : '{self.name}' ==")
      print(f"Status: {self.status}")
      if (self.reasons != []):
        print(f"Detailed data:")
        for i in range(len(self.reasons)):
          print(f" - {self.get_fail_severity_color(self.reasons[i][1])}"\
                f"{self.get_fail_severity_emoji(self.reasons[i][1])}  ➜  {self.reasons[i][0]}{Back.RESET + Fore.RESET}")
      print("==\n")

    def to_dict(self) -> dict:
      return {
        "name": self.name,
        "status": self.status_int,
        "reasons": self.reasons
      }

  def __init__(self, parser: GrindScript_Parser):
    self.test_results: list[tuple[str, list[GrindScript_Executer.GrindScript_TestResults]]] = []
    self.parser: GrindScript_Parser = parser
    self.success: bool = True
    self.run_start_time: datetime = datetime.now()
    self.json_log: dict[str, Type[Any | datetime | str | list]] = {
      "exec_epoch": floor(self.run_start_time.timestamp()),
      "exec_date": f"{self.run_start_time}",
      "reports": []
    }
    if (parser == None):
      message: str = "No parser has been supplied, cannot continue"
      print(gs_excepts_failstr(message))
      exit(EXIT_FAIL)
    self.gs_suite_exec()
    self.gs_suites_print()
    self.gs_tests_update_sf_state()
    self.gs_fill_reports()

  def gs_suite_exec(self):
    print(f"====== INITIALIZING TESTS ======\n")
    for i in range(self.parser.n_suites):
      print(f"=== SUITE '{self.parser.suites[i].s_name}' ===\n")
      self.test_results.append((self.parser.suites[i].s_name, []))
      for j in range(self.parser.suites[i].s_tests_len):
        test_name = self.parser.suites[i].cmpl_tests[j].t_name
        print(f"== TEST '{self.parser.suites[i].cmpl_tests[j].t_name}' ==")
        grinder = self.GrindScript_Valgrinder(self.parser.suites[i].cmpl_tests[j].t_name,
                                              self.parser.suites[i].cmpl_tests[j].e_name,
                                              self.parser.suites[i].cmpl_tests[j].e_args)
        results = grinder.exec()
        self.test_results[i][1].append(self.GrindScript_TestResults(test_name, results.status,
                                                                    results.report))
        print(f"== TEST COMPLETE ==\n")
      print(f"=== SUITE COMPLETE ===\n")
    print(f"====== TESTS ENDED ======\n")

  def gs_suites_print(self):
    for i in range(len(self.test_results)):
      self.gs_suite_print(self.test_results[i])

  def gs_suite_print(self, test_results: tuple[str, list[GrindScript_TestResults]]):
    print(f"=== SUITE RESULTS : '{test_results[0]}' ===\n")
    for j in range(len(test_results[1])):
      test_results[1][j].print()
    pb = Grindme_ProgressBar()
    ratio: tuple[int, int] = self.gs_tests_get_sf_ratio(test_results[1])
    pb.progress = (ratio[0] / ratio[1]) * 100
    print(f"Percentages of suite '{test_results[0]}':")
    pb.pb_print()
    print("===\n")

  def gs_fill_reports(self) -> None:
    for suite in self.test_results:
      if (suite[1] == []):
        continue
      for test in suite[1]:
        self.json_log['reports'].append(test.to_dict())

  def gs_tests_update_sf_state(self) -> None:
    for suite in self.test_results:
      if (suite[1] == []):
        continue
      for test in suite[1]:
        if (test.status_int != STATUS_OK):
          self.success = False
          return None
    self.success = True
    return None

  def gs_tests_get_sf_ratio(self, tests: list[GrindScript_TestResults]) -> tuple[int, int]:
    n_tests = len(tests)
    success = 0
    for test in tests:
      if (test.status_int == STATUS_OK):
        success += 1
    return (success,  n_tests)
