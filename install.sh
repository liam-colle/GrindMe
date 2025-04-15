#!/bin/bash
GREEN="\e[32m"
YELLOW="\e[33m"
RED="\e[31m"
ENDCOLOR="\e[0m"

RM=rm
GIT_COMMAND=git
PYTHON3_COMMAND=python3
VALGRIND_COMMAND=valgrind

## Check required commands
if ! command -v $GIT_COMMAND 2>&1 >/dev/null
then
    echo -e "${YELLOW}${GIT_COMMAND}${RED} could not be found!${ENDCOLOR}\nPlease install the ${YELLOW}${GIT_COMMAND}${ENDCOLOR} package."
    exit 1
fi

if ! command -v $PYTHON3_COMMAND 2>&1 >/dev/null
then
    echo -e "${YELLOW}${PYTHON3_COMMAND}${RED} could not be found!${ENDCOLOR}\nPlease install the ${YELLOW}${PYTHON3_COMMAND}${ENDCOLOR} package."
    exit 1
fi

if ! command -v $VALGRIND_COMMAND 2>&1 >/dev/null
then
    echo -e "${YELLOW}${VALGRIND_COMMAND}${RED} could not be found!${ENDCOLOR}\nPlease install the ${YELLOW}${VALGRIND_COMMAND}${ENDCOLOR} package."
    exit 1
fi

$RM -rf /tmp/grindme-installer
if ! git clone --depth=1 https://github.com/liam-colle-archivist/GrindMe.git /tmp/grindme-installer 2> /dev/null; then
    echo -e "${RED}${GIT_COMMAND} could not clone the repository.\n${YELLOW}Check your connection to github.${ENDCOLOR}"
    exit 1
fi
/tmp/grindme-installer/install_system.sh
$RM -rf /tmp/grindme-installer
