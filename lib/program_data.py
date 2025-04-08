import os

# Critical Program Data
NAME: str = "GrindMe"
DESCRIPTION: str = "an automatic valgrind tester for your DevOps or laziness needs."
START_MSG: str =\
  f"{NAME}, {DESCRIPTION}\n" +\
  f"Copyright (C) 2025 under license GNU GPL v3, made by Liam Colle\n" +\
  f"{'-' * os.get_terminal_size().columns}\n" +\
  f"This program uses 'valgrind' as the reference memchecker\n" +\
  f"Copyright (C) 2002-2022, and GNU GPL'd, by Julian Seward et al.\n" +\
  f"{'-' * os.get_terminal_size().columns}"
VERSION: str = "v0.0.0"

# Script File Generator
DEF_SCRIPT_PATH = "./.grindme/"
DEF_SCRIPT_NAME = "config.json"
DEF_SCRIPT_INDENT = 2
EXAMPLE_SCRIPT: object = \
{
  "launch_opts": {
    "strict": False
  },
  "suites": [
    {
      "name": "<name>",
      "tests": [
        {
          "name": "<name>",
          "description": "<description>",
          "executable": "<filename>",
          "args": [],
          "opts": {
            "redirect_stdout": None,
            "pretest_cmd": ["<command_before_test>", "[optional_args]"],
            "posttest_cmd": ["<command_before_test>", "[optional_args]"]
          }
        }
      ],
      "opts": {
        "pretest_cmd": ["<command_before_suite>", "[optional_args]"],
        "posttest_cmd": ["<command_before_suite>", "[optional_args]"]
      }
    }
  ]
}

## Checker Statuses
STATUS_OK = 0
STATUS_KO = 1
STATUS_CRASH = 2

## Checker Severities
SEV_INFO = 0
SEV_MINOR = 1
SEV_MAJOR = 2
SEV_CRITICAL = 3

## List of Valgrind Errors
VALGRIND_ERRORS: list[tuple[str, str, int]] = [
  # (Match Regex String: str, Message: str, Severity: int)

  # FILE NOT FOUND
  (r"^valgrind:(.*): No such file or directory$", "File not found", SEV_MINOR),

  # INVALID READ
  (r"^(.*)Invalid read of(.*)size$", "Invalid memory read", SEV_MAJOR),

  # INVALID WRITE
  (r"^(.*)Invalid write of(.*)size$", "Invalid memory write", SEV_MAJOR),

  # CONDITIONAL JUMP ON UNINITIALIZED VALUES
  (r"^(.*)Conditional jump or move depends on uninitialised value\(s\)$", "Conditional jump on uninitialized values", SEV_MINOR),

  # SYSCALL PARAM POINTS TO UNINITIALIZED
  (r"^(.*)Syscall param(.*)contains uninitialised byte\(s\)$", "Syscall parameter points to uninitialized values", SEV_MAJOR),

  # INVALID FREE
  (r"^(.*)Invalid free\(\)$", "Invalid free operation", SEV_MAJOR),

  # MISMATCHED FREE
  (r"^(.*)Mismatched free\(\) / delete / delete \[\]$", "Mismatched free function", SEV_MAJOR),

  # SRC & DEST OVERLAP
  (r"^(.*)Source and destination overlap in (.*)$", "Source and destination overlap in function", SEV_MAJOR),

  # FISHY ARG VALUES
  (r"^(.*)Argument (.*) of function (.*) has a fishy (possibly negative) value: (.*)$", "Source and destination overlap in function", SEV_MAJOR),

  # REALLOC SIZE ZERO
  (r"^(.*)realloc() with size 0$", "Source and destination overlap in function", SEV_MINOR),

  # INVALID ALIGNMENT
  (r"^(.*)Invalid alignment value:(.*)$", "Source and destination overlap in function", SEV_MINOR),

  # UNRECOGNIZED INSTRUCTION
  (r"^(.*)Unrecognised instruction at address(.*)$", "Source and destination overlap in function", SEV_CRITICAL),

  # CRASH
  (r"^(.*)Process terminating with default action of signal (.*) \((SIGSEGV|SIGILL|SIGABRT|SIGIOT|SIGBUS|SIGFPE|SIGKILL|SIGXCPU|SIGXFSZ|SIGSYS|SIGUNUSED)\)(.*)$",
   "Abnormal termination", SEV_CRITICAL),
]

VALGRIND_MEMLEAK = (
  "Memory Leak", SEV_MINOR
)
