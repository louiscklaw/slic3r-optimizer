#!/usr/bin/env bash

set -ex

~/AppImage/PrusaSlicer-2.2.0+linux-x64-202003211856.AppImage --export-gcode --repair ./test_slic3r.stl

grep -i "filament used \[mm\]" test_slic3r.gcode


~/AppImage/PrusaSlicer-2.2.0+linux-x64-202003211856.AppImage --rotate-x=45 --rotate-y=45 --export-gcode --repair ./test_slic3r.stl

grep -i "filament used \[mm\]" test_slic3r.gcode
