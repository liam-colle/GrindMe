# GrindMe

**An automatic valgrind tester for your DevOps or laziness needs.**

![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54&label=3.11.12)
[![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=flat&logo=githubactions&logoColor=white)](https://github.com/liam-colle-archivist/GrindMe/actions)
[![GrindMe CD/CI](https://github.com/liam-colle-archivist/GrindMe/actions/workflows/actions.yml/badge.svg)](https://github.com/liam-colle-archivist/GrindMe/actions/workflows/actions.yml)
![GPL v3](https://img.shields.io/badge/license-GPLv3-blue?style=flat)

## Description

GrindMe allows you to setup a custom json script that will launch automated valgrind tests
and report them in the way you'd like (Plaintext, JSON Output, etc...).
By default, GrindMe doesn't test anything unless specified.

## Installation

### Requirements

* valgrind
* git
* python3
  * ``py3`` for alpine users
* python3-venv
  * ``py3-venv`` for alpine users

### How to install?

```shell
curl -B https://raw.githubusercontent.com/liam-colle-archivist/GrindMe/refs/heads/main/install.sh | bash
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

Configuration should be stored in a ``.grindme`` directory and the configuration file should be named ``config.json``
if you want to run GrindMe in "automatic mode" / without any arguments.

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

### Docker

GrindMe comes shipped with a Docker image on Docker Hub.

``liamcollearchivist/grindme`` - [DockerIO Repository](https://hub.docker.com/repository/docker/liamcollearchivist/grindme)

GrindMe offers 3 types of images

* ``latest``

  An image running on Ubuntu (``ubuntu:latest``) which only comes supplied with the bare minimum for GrindMe to function.

  * Compressed Size: ~170 MB
  * Local run script: ``docker run -v ./:/grindme -it --rm liamcollearchivist/grindme /bin/bash``
  > ⚠️ - Additional build packages must be installed manually by creating another Docker image based on this one,
    or using your CD/CI workflow tool.

* ``alpine-latest``
  An image running on Alpine (``alpine:latest``) which only comes supplied with the bare minimum for GrindMe to function.

  * Compressed Size: ~70 MB
  * Local run script: ``docker run -v ./:/grindme -it --rm liamcollearchivist/grindme:alpine-latest /bin/bash``
  > ⚠️ - Additional build packages must be installed manually by creating another Docker image based on this one,
    or using your CD/CI workflow tool.

* ``epitech-latest``
  An image running on Ubuntu using the official Epitech 'Epitest' docker (``epitechcontent/epitest-docker``)
  which comes with the bare minimum for GrindMe to function alongside everything that Epitech needs to use their 'moulinette'.

  * Compressed Size: ~1.85 GB
  * Local run script: ``docker run -v ./:/grindme -it --rm liamcollearchivist/grindme:epitech-latest /bin/bash``

### CD/CI - ``GitHub Actions``

The GrindMe docker can be invoked in a job within a GitHub Actions workflow.

> ⚠️ - This however requires a customized setup due to limitations of valgrind applying to Docker containers.
  This is due to the fact that valgrind requires the file descriptors to be limited to a low amount, or else it will refuse to execute.
  As of now we haven't found a way to statically set the ulimit in the image directly.
  Therefore, a 'ulimit' option has been added in the container invokation options in the job to ensure that the docker
  executes with the right permissions.
  We do not know what going above 1024 does, as we've never tried it yet. At your own risk! ``¯\_(ツ)_/¯``

```yaml
name: GrindMe Test

on: [push, pull_request]

jobs:
  run_grind_me:
    runs-on: ubuntu-latest
    container:
      image: liamcollearchivist/grindme:epitech-latest
      options: --ulimit nofile=1024:1024

    steps:
    - name: "[GITHUB] Checkout code from GitHub"
      uses: actions/checkout@v4

    # < Compile or get your program here

    - name: "[TESTS] Execute tests"
      run: grindme --github-action

    # < Do your teardown here
```

[GrindMe](https://github.com/liam-colle-archivist/GrindMe) by [Liam Colle](https://github.com/liam-colle-archivist) is licensed under GPL v3.
