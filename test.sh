#!/usr/bin/env bash

set -ex

# pipenv run python3 ./slic3r_optimize.py /home/logic/_workspace/slic3r-optimizer/test_slic3r.stl

# /home/logic/_workspace/opendps-tryout/hardware/STLs/maincase.stl
pipenv run python3 ./slic3r_optimize.py /home/logic/_workspace/opendps-tryout/hardware/STLs/maincase.stl
