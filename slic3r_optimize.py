#!/usr/bin/env python3

import os,sys, subprocess
from pprint import pprint
from string import Template

ANGLE_LIST=range(0,360,90)
print(len(list(ANGLE_LIST)))

if len(sys.argv) < 2:
  print('no stl file defined')
  sys.exit(99)

target_stl_file = sys.argv[1]



TEST_COMMAND = Template('''/home/logic/AppImage/PrusaSlicer-2.2.0+linux-x64-202003211856.AppImage --datadir ~/3dprinter-config/Slic3r-settings --rotate $z_angle --rotate-x $x_angle --rotate-y $y_angle --export-3mf --export-gcode --repair --support-material --support-material-auto --center 100,100 --output /tmp /tmp/optimize.stl''')

three_mf_filename = Template("")
cwd_3mf_filename = Template('{}/test_$x_angle_$yangle_$z_angle.3mf'.format(os.getcwd()))

result_list = {}

def copy_stl_to_tmp(target_stl_file):
  cp_command = 'cp {} /tmp/optimize.stl'.format(target_stl_file)
  subprocess.check_output(cp_command.split(' '))

def get_mf_filename(x_angle, y_angle, z_angle):
  return "test_x{}_y{}_z{}.3mf".format(x_angle, y_angle, z_angle)

def get_3mf_filename_with_filament(x_angle, y_angle, z_angle, filament_used):
  return "test_x{}_y{}_z{}_f{}.3mf".format(x_angle, y_angle, z_angle, filament_used)

def get_tmp_three_mf_filename(x_angle, y_angle, z_angle):
  return "/tmp/{}".format(get_mf_filename(x_angle, y_angle, z_angle))

def get_cwd_three_mf_filename(x_angle, y_angle, z_angle, filament_used):
  return '{}/{}'.format(os.getcwd(), get_3mf_filename_with_filament(x_angle, y_angle, z_angle, filament_used))

def get_run_config():
  run_config = []
  for x_angle in ANGLE_LIST:
    for y_angle in ANGLE_LIST:
      for z_angle in ANGLE_LIST:
        _3mf_filename = get_tmp_three_mf_filename(x_angle, y_angle, z_angle)
        run_config.append((x_angle, y_angle, z_angle, _3mf_filename))


  print('{} conbination to test'.format(len(run_config)))
  return run_config

def run_slic3r(x,y,z):
  result = subprocess.check_output(TEST_COMMAND.substitute(z_angle=z, y_angle=y, x_angle=x).split(' '))
  return result

def store_generated_3mf(target_filename):
  mv_command = "mv {} {}".format("/tmp/optimize.3mf", target_filename)
  subprocess.check_output(mv_command.split(' '))

def rename_3mf_file(target_filename):
  return subprocess.check_output('mv /tmp/optimize.3mf {}/{}'.format(os.getcwd(), target_filename))

def check_filament_used(gcode_path):
  with open(gcode_path,'r') as f_gcode:
    used_filament = filter(lambda x: x.find('filament used [mm]')>0, f_gcode.readlines())
    mm_in_text = list(used_filament)[0].strip().replace('; filament used [mm] = ','')
    return mm_in_text

copy_stl_to_tmp(target_stl_file)

test_count = 0
for run_config in get_run_config():
  (x_angle, y_angle, z_angle, _3mf_filename) = run_config
  run_slic3r(x_angle, y_angle, z_angle)
  store_generated_3mf(_3mf_filename)

  filament_used = check_filament_used('/tmp/optimize.gcode')
  print(f'testing x angle {x_angle}, y_angle {y_angle}, z_angle {z_angle}: filament used"{filament_used}"')

  if (filament_used in result_list.keys()):
    result_list[filament_used].append((x_angle, y_angle,z_angle, _3mf_filename))
  else:
    result_list[filament_used] = [(x_angle, y_angle, z_angle, _3mf_filename)]

  test_count+=1

filament_min_to_max = sorted(map(lambda x: float(x), result_list.keys()))
print('sorting filament from min to max')
print(filament_min_to_max)
for i in filament_min_to_max[0:5-1]:
  for (x_angle, y_angle, z_angle, tmp_3mf_filename) in result_list[str(i)]:
    # print(result_list[str(i)])
    # tmp_filename = get_tmp_three_mf_filename(x_angle, y_angle, z_angle)
    cwd_filename = get_cwd_three_mf_filename(x_angle, y_angle, z_angle, str(i).replace('.','_'))
    mv_command = 'mv {} {}'.format(tmp_3mf_filename,cwd_filename)
    subprocess.check_output(mv_command.split(' '))

  # print(filament_min_to_max[i])
  # print("filament used {}, combination {}".format(i, ' '.join(filament_min_to_max[str(i)])))
