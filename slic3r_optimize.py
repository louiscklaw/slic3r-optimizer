#!/usr/bin/env python3

import os,sys, subprocess
from pprint import pprint
from string import Template

ANGLE_LIST=[0,90,180]

pprint("helloworld")

TEST_COMMAND = Template('''/home/logic/AppImage/PrusaSlicer-2.2.0+linux-x64-202003211856.AppImage --datadir ~/3dprinter-config/Slic3r-settings --rotate $z_angle --rotate-x $x_angle --rotate-y $y_angle --export-gcode --repair --output /tmp ./test_slic3r.stl''')

def gen_gcode_with_angle(x,y,z):
  return subprocess.check_output(TEST_COMMAND.substitute(
  z_angle=z, y_angle=y, x_angle=x
).split(' '))

def check_filament_used(gcode_path):
  with open(gcode_path,'r') as f_gcode:
    used_filament = filter(lambda x: x.find('filament used [mm]')>0, f_gcode.readlines())
    return list(used_filament)[0].strip().replace('; filament used [mm]','')

test_count = 0
for x_angle in ANGLE_LIST:
  for y_angle in ANGLE_LIST:
    for z_angle in ANGLE_LIST:
      gen_gcode_with_angle(x_angle, y_angle, z_angle)
      filament_used = check_filament_used('/tmp/test_slic3r.gcode')
      print(f'testing x angle {x_angle}, y_angle {y_angle}, z_angle {z_angle}: filament used"{filament_used}"')
      test_count+=1



print(f'total combination tested {test_count}')