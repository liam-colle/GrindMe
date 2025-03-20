import argparse, json, os
from lib.grindscript_parse import GrindScript_Parser
from lib.grindscript_exec import GrindScript_Executer
from lib.grindscript_githubactions import GrindScript_GithubActions
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
  except FileExistsError:
    print("OOps, f ile exists")
  except Exception as e:
    print(e)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    prog = NAME,
    description = DESCRIPTION,
  )
  parser.add_argument(
    "filename",
    type = str,
    nargs = "?"
  )
  parser.add_argument(
    "-d",
    "--docker",
    action = "store_true"
  )
  parser.add_argument(
    "-s",
    "--strict",
    action = "store_true"
  )
  parser.add_argument(
    "-g",
    "--generate-file",
    action = "store_true"
  )
  parser.add_argument(
    "-v",
    "--verbose",
    action = "store_true"
  )
  args: object = parser.parse_args()
  print(START_MSG)
  if (args.verbose):
    print_command_headers(args)
  if (args.generate_file):
      generate_file()
  gs_parser = GrindScript_Parser("testdir/.grindme/config.json" if args.docker else ".grindme/config.json")
  gs_exec = GrindScript_Executer(gs_parser)
  gs_ga = GrindScript_GithubActions(gs_exec.json_log)
  gs_ga.actionify()
  gs_ga.dump_ga_annotations()
  if (gs_exec.success == False):
    exit(1)
  exit(0)
