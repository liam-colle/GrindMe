#!/usr/bin/bash
GREEN="\e[32m"
YELLOW="\e[33m"
RED="\e[31m"
ENDCOLOR="\e[0m"

sudo bash -c """\
    set -e
    echo -e '===== GRINDME INSTALLER (LOCAL) =====';\
    echo -e '=== 1 - ${YELLOW}INSTALLING CORE FILES${ENDCOLOR} ===';\
    echo -e '=== 1 >> ${GREEN}OK${ENDCOLOR} ===';\
    echo "";\
    echo -e '=== 2 - ${YELLOW}INSTALLING VIRTUAL ENVIRONMENT${ENDCOLOR} ===';\
    python3 -m venv .venv;\
    source .venv/bin/activate;\
    echo -e '=== 2 >> ${GREEN}OK${ENDCOLOR} ===';\
    echo "";\
    echo -e '=== 3 - ${YELLOW}INSTALLING DEPENDENCIES${ENDCOLOR} ===';\
    python3 -m pip install -r requirements.txt;\
    echo -e '=== 3 >> ${GREEN}OK${ENDCOLOR} ===';\
    echo "";\
    echo -e '=== 4 - ${YELLOW}FINALIZING${ENDCOLOR} ===';\
    echo -e '=== 4 >> ${GREEN}OK${ENDCOLOR} ===';\
    echo "";\
    echo GrindMe has been successfully installed / updated!;\
"""
