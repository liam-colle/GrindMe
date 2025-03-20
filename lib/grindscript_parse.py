import json
from lib.exceptions import\
  gs_excepts_failstr,\
  GSP_CouldNotLoadJSON,\
  GSP_JSONParseError
from lib.exit_codes import\
  EXIT_PARSER_FAIL,\
  EXIT_JSON_FAIL

class GrindScript_Parser:
  class GrindScript_Suite:
    class GrindScript_Test:
        def __init__(self, suite_dat: tuple[str, int], data: dict, docker_mode: bool = False):
          try:
            self.t_name: str = data["name"]
            self.t_desc: str = data["description"]
            self.e_name: str = data["executable"]
            if (docker_mode == True):
              self.e_name = f"testdir/{self.e_name}"
            self.e_args: list[str] = data["args"]
          except KeyError as e:
            message = f"Missing mandatory key '{e.args[0]}' in Suite {suite_dat[0]} Test n°{suite_dat[1]}"
            print(gs_excepts_failstr(message))
            exit(EXIT_JSON_FAIL)

    def __init__(self, n: int, data: str, docker_mode: bool = False):
      try:
        self.s_name: str = data["name"]
        self.s_tests: dict = data["tests"]
        self.s_tests_len = len(self.s_tests)
        self.docker_mode = docker_mode
      except KeyError as e:
        message = f"Missing mandatory key '{e.args[0]}' in Suite n°{n}"
        print(gs_excepts_failstr(message))
        exit(EXIT_JSON_FAIL)
      self.cmpl_tests: list[GrindScript_Parser.GrindScript_Suite.GrindScript_Test] = []

      if (len(self.s_tests) <= 0):
        message = f"No tests in Suite n°{n}"
        print(gs_excepts_failstr(message))
        exit(EXIT_JSON_FAIL)
      for i in range(len(self.s_tests)):
        self.cmpl_tests.append(self.GrindScript_Test((self.s_name, i + 1), self.s_tests[i]))


  def __init__(self, filename: str, docker_mode: bool = False):
    self.json: object = None
    self.n_suites: int = 0
    self.suites: list[GrindScript_Parser.GrindScript_Suite] = []
    self.docker_mode = docker_mode

    try:
      file = open(filename, "r")
      contents = file.read()
      self.json = json.loads(contents)
    except FileNotFoundError:
      print(GSP_CouldNotLoadJSON(f"Script file does not exist: '{filename}'"))
      exit(EXIT_PARSER_FAIL)

    for i in range(len(self.json["suites"])):
      self.suites.append(self.GrindScript_Suite(i, self.json["suites"][i], ))
    self.n_suites = len(self.suites)