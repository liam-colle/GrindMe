#!/bin/bash
sudo bash -c """\
    echo Uninstalling grindme...;\
    rm -r /usr/share/grindme;\
    unlink /usr/bin/grindme;\
    echo GrindMe has been successfully uninstalled!;\
"""
