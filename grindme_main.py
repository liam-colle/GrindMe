import argparse, json, os
from sys import stderr
from lib.exit_codes import\
  EXIT_SUCCESS,\
  EXIT_FAIL
from lib.grindscript_parse import GrindScript_Parser
from lib.grindscript_exec import GrindScript_Executer
from lib.grindscript_githubactions import GrindScript_GithubActions
from lib.exceptions import GSE_ExecutionError, gs_excepts_panicstr
from lib.program_data import\
  NAME,\
  DESCRIPTION,\
  START_MSG,\
  DEF_SCRIPT_NAME,\
  DEF_SCRIPT_PATH,\
  DEF_SCRIPT_INDENT,\
  EXAMPLE_SCRIPT

def print_command_headers(args: object):
  print(
    "Command: " + f"{args.filename}\n" +\
    "Is Strict: " + f"{args.strict}\n" +\
    "Is Verbose: " + f"{args.verbose}\n"
  )

def generate_file():
  try:
    ## Prompts
    pr_outpath = input(f"Path to grindme directory [Default: {DEF_SCRIPT_PATH}]") or DEF_SCRIPT_PATH
    pr_outname = input(f"Name of script file [Default: {DEF_SCRIPT_NAME}]") or DEF_SCRIPT_NAME
    try:
      pr_indents = int(input(f"Number of indents [Default: {DEF_SCRIPT_INDENT}]") or DEF_SCRIPT_INDENT)
    except ValueError:
      pr_indents = 2

    ## Writer
    if (not os.path.exists(pr_outpath)):
      os.makedirs(pr_outpath)
    file = open(f"{pr_outpath}/{pr_outname}", "w")
    file.write(json.dumps(EXAMPLE_SCRIPT, indent = pr_indents))
    file.close()
  except FileNotFoundError:
    message = f"GrindScript file \"{pr_outpath}/{pr_outname}\" not found"
    print(gs_excepts_panicstr(message), file = stderr)
    exit(EXIT_FAIL)
  except Exception as e:
    message = f"An unknown exception occured:\n{e}"
    print(gs_excepts_panicstr(message), file = stderr)
    exit(EXIT_FAIL)


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
    generate_file()
  gs_parser = GrindScript_Parser(".grindme/config.json")
  gs_exec = GrindScript_Executer(gs_parser)
  if (args.github_action):
    gs_ga = GrindScript_GithubActions(gs_exec.json_log)
    gs_ga.actionify()
    gs_ga.dump_ga_annotations()
  if (gs_exec.success == False):
    exit(EXIT_SUCCESS)
  exit(EXIT_FAIL)
