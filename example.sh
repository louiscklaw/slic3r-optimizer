#!/usr/bin/env bash

set -x

# /home/logic/_workspace/voron-sfx/my-parts/4020-fan-cover/print.stl

rm -rf /home/logic/_workspace/slic3r-optimizer/*.3mf

set -ex

# /home/logic/_workspace/opendps-tryout/hardware/STLs/maincase.stl
pipenv run python3 ./slic3r_optimize.py /home/logic/_workspace/voron-sfx/my-parts/4020-fan-cover/print.stl
