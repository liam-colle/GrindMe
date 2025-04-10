#!/bin/bash
GREEN="\e[32m"
YELLOW="\e[33m"
RED="\e[31m"
ENDCOLOR="\e[0m"

COMMAND_CHAIN="""\
    set -e
    echo -e '===== GRINDME INSTALLER =====';\
    echo -e '=== 1 - ${YELLOW}INSTALLING CORE FILES${ENDCOLOR} ===';\
    rm -rf /usr/share/grindme
    rm -rf /usr/bin/grindme
    mkdir /usr/share/grindme;\
    cp -r * /usr/share/grindme/;\
    echo -e '=== 1 >> ${GREEN}OK${ENDCOLOR} ===';\
    echo "";\
    echo -e '=== 2 - ${YELLOW}INSTALLING VIRTUAL ENVIRONMENT${ENDCOLOR} ===';\
    python3 -m venv /usr/share/grindme/.venv;\
    source /usr/share/grindme/.venv/bin/activate;\
    echo -e '=== 2 >> ${GREEN}OK${ENDCOLOR} ===';\
    echo "";\
    echo -e '=== 3 - ${YELLOW}INSTALLING DEPENDENCIES${ENDCOLOR} ===';\
    python3 -m pip install -r requirements.txt;\
    echo -e '=== 3 >> ${GREEN}OK${ENDCOLOR} ===';\
    echo "";\
    echo -e '=== 4 - ${YELLOW}FINALIZING${ENDCOLOR} ===';\
    ln /usr/share/grindme/grindme /usr/bin/grindme;\
    echo -e '=== 4 >> ${GREEN}OK${ENDCOLOR} ===';\
    echo "";\
    echo GrindMe has been successfully installed / updated!;\
"""

if [ $(id -u) -ne 0 ]
then
    sudo bash -c "${COMMAND_CHAIN}"
else
    bash -c "${COMMAND_CHAIN}"
fi