# GrindMe

**An automatic valgrind tester for your DevOps or laziness needs.**

## Description

GrindMe allows you to setup a custom json script that will launch automated valgrind tests
and report them in the way you'd like (Plaintext, JSON Output, etc...).
By default, GrindMe doesn't test anything unless specified.

## Installation

```shell
TBD
```

## Features

* Highly Customizable JSON script
* Multiple ways to print out or export test results

## Usage

### Program Arguments

```shell
grindme [path-to-executable]
```

### Configuration

Configuration should be stored in a ``.grindme`` directory and the configuration file should be named ``config.json``.

### Script Examples

*Note: The program does not support JSON with comments. Parts of it are commented for demonstration purposes only.*

#### Test : ``Single Program`` - ``mytest``

#### JSON

```json
{
  "TBD": true
}
```

#### Example Console Output

```shell
TBD
```
