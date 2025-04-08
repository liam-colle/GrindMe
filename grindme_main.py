import argparse, json, os
from sys import stderr
from lib.exit_codes import\
  EXIT_SUCCESS,\
  EXIT_FAIL
from lib.grindscript_parse import GrindScript_Parser
from lib.grindscript_exec import GrindScript_Executer
from lib.grindscript_githubactions import GrindScript_GithubActions
from lib.grindscript_scriptgen import GrindScript_ScriptGenerator
from lib.grindscript_reportdumper import GrindScript_ReportDumper, gs_identify_dump
from lib.exceptions import GSE_ExecutionError, gs_excepts_panicstr
from lib.program_data import\
  NAME,\
  DESCRIPTION,\
  START_MSG,\
  DEF_SCRIPT_NAME,\
  DEF_SCRIPT_PATH

def print_command_headers(args: object):
  print(
    "Command: " + f"{args.filename}\n" +\
    "Is Strict: " + f"{args.strict}\n" +\
    "Is Verbose: " + f"{args.verbose}\n"
  )

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    prog = NAME,
    description = DESCRIPTION,
  )
  parser.add_argument(
    "filename",
    type = str,
    nargs = "?",
  )
  parser.add_argument(
    "--dump-report",
    type = str,
    nargs = "?",
    const = ""
  )
  parser.add_argument(
    "--dump-report-type",
    type = str,
    nargs = "?",
  )
  parser.add_argument(
    "--github-action",
    action = "store_true",
  )
  parser.add_argument(
    "-s",
    "--strict",
    action = "store_true",
  )
  parser.add_argument(
    "-g",
    "--generate-file",
    action = "store_true",
  )
  parser.add_argument(
    "-v",
    "--verbose",
    action = "store_true",
  )
  args: object = parser.parse_args()
  print(START_MSG)
  if (args.verbose):
    print_command_headers(args)
  if (args.generate_file):
    generator = GrindScript_ScriptGenerator()
    generator.write()
    exit(EXIT_SUCCESS)
  gs_parser = GrindScript_Parser(args.filename or DEF_SCRIPT_PATH + DEF_SCRIPT_NAME)
  gs_exec = GrindScript_Executer(gs_parser)
  if (args.github_action):
    gs_ga = GrindScript_GithubActions(gs_exec.json_log)
    gs_ga.actionify()
    gs_ga.dump_ga_annotations()
  if (args.dump_report is not None):
    dumper = GrindScript_ReportDumper(gs_exec.json_log, args.dump_report,
                                      gs_identify_dump(args.dump_report_type))
    dumper.write()
  if (gs_exec.success == False):
    exit(EXIT_SUCCESS)
  exit(EXIT_FAIL)
