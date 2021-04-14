#!/bin/sh

cd alpha/sage
MPMATH_SAGE=1 PYTHONPATH=`pwd` sage -c 'load("../../pluto_stnfs.py")'
