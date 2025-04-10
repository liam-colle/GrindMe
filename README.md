# GrindMe

**An automatic valgrind tester for your DevOps or laziness needs.**

## Description

GrindMe allows you to setup a custom json script that will launch automated valgrind tests
and report them in the way you'd like (Plaintext, JSON Output, etc...).
By default, GrindMe doesn't test anything unless specified.

## Installation

### Requirements

* rcheck
* git
* python3
  * ``py3`` for alpine users
* python3-venv
  * ``py3-venv`` for alpine users

### How to install?

```shell
curl -B https://raw.githubusercontent.com/Charlito33/rCheck2/refs/heads/master/install.sh | bash
```

## Features

* Highly Customizable JSON script
* Multiple ways to print out or export test results

## Usage

### Program

```plaintext
usage: GrindMe [-h] [--dump-report [DUMP_REPORT]] [--dump-report-type [DUMP_REPORT_TYPE]] [--github-action] [-s] [-g] [-v] [filename]

An automatic valgrind tester for your DevOps or laziness needs.

positional arguments:
  filename

options:
  -h, --help            show this help message and exit
  --dump-report [DUMP_REPORT]
  --dump-report-type [DUMP_REPORT_TYPE]
  --github-action
  -s, --strict
  -g, --generate-file
  -v, --verbose
```

### Configuration

Configuration should be stored in a ``.grindme`` directory and the configuration file should be named ``config.json``.

The json scripts should be structured like the following:

```json
{
  "suites": [
    {
      "name": "Test mytest",
      "tests": [
        {
          "name": "Test 1",
          "description": "Check if program works",
          "executable": "./mytest",
          "args": [],
          "input_file": null
        }
      ]
    }
  ]
}
```

* ``suites``: The suites used by grindme ``(list: (object))``
  * ``name``: The name of the suite ``(string)``
  * ``tests``: The name of the suite ``(list: (object))``
    * ``name``: The name of the test ``(string)``
    * ``description``: The description of the test ``(string)``
    * ``executable``: The executable used by the test ``(string)``
    * ``description``: The description of the test ``(string)``
    * ``args``: The arguments used by the test ``(list: (string))``
    * ``input_file``: A file to pipe into the stdin buffer of the program ``(string | null)`` ``[optional]``

### Script Examples

*Note: The program does not support JSON with comments. Parts of it are commented for demonstration purposes only.*

#### Test : ``Single Program`` - ``mytest``

##### JSON

```json
{
  "suites": [
    {
      "name": "Test mytest",
      "tests": [
        {
          "name": "Test 1",
          "description": "Check if program works",
          "executable": "./mytest",
          "args": [],
          "input_file": null
        }
      ]
    }
  ]
}
```

##### Example Console Output

```plaintext
=== SUITE RESULTS : 'Test mytest' ===

== TEST RESULTS : 'Test 1' ==
Status: OK
==

Percentages of suite 'Test mytest':
[=====================================] - 100.0%
===
```

#### Test : ``Single Program`` - ``mytest`` with many errors

##### JSON

```json
{
  "suites": [
    {
      "name": "Test mytest",
      "tests": [
        {
          "name": "Test 1",
          "description": "Check if program works",
          "executable": "./mytest",
          "args": [],
          "input_file": null
        }
      ]
    },
    {
      "name": "Test mytest (CRASH)",
      "tests": [
        {
          "name": "Test 1",
          "description": "Check if program works",
          "executable": "./mytest",
          "args": ["-f", "./tests/test.txt"],
          "input_file": null
        },
        {
          "name": "Test 2",
          "description": "Check if program works",
          "executable": "./mytest",
          "args": ["-f", "./tests/test.txt", "-e"],
          "input_file": "./tests/nothing.txt"
        }
      ]
    }
  ]
}
```

##### Example Console Output

```plaintext
=== SUITE RESULTS : 'Test mytest' ===

== TEST RESULTS : 'Test 1' ==
Status: OK
==

Percentages of suite 'Test mytest':
[=====================================] - 100.0%
===

=== SUITE RESULTS : 'Test mytest (CRASH)' ===

== TEST RESULTS : 'Test 1' ==
Status: KO
Detailed data:
 - ⚠️  ➜  Conditional jump on uninitialized values
 - ⚠️  ➜  Memory Leak
==

== TEST RESULTS : 'Test 2' ==
Status: CRASH
Detailed data:
 - ⚠️  ➜  Conditional jump on uninitialized values
 - ⚠️  ➜  Abnormal termination
 - ⚠️  ➜  Memory Leak
==

Percentages of suite 'Test mytest (CRASH)':
[                                     ] - 0.0%
===
```
