#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  grid-search-treeseg.py
#  
#  Copyright 2021 Santiago <santiagobanchero@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from subprocess import run, PIPE, CalledProcessError
from sys import argv
from glob import glob
import os 
import datetime
import sqlite3


IN_PCL_TILE = argv[1]
IN_coords = argv[2]
db_config = argv[3]
DIR_ROOT = argv[4]

query_exp = "SELECT edgelength, resolution, percentil, zmin, zmax, smooth, dmin, dmax, d.id, g.id, f.id FROM downsample d, getdemslice g, findstems f LIMIT 10"


def get_downsample_file(DIR_ROOT):
    path_lst = [x for x in glob(DIR_ROOT+"/*") if 'downsample' in x]
	return path_lst[0]

def get_slice_file(DIR_ROOT):
    return [x for x in glob(DIR_ROOT+"/*") if 'slice' in x][0]



def new_running_dir():
	# Start with new experiment
	MAIN_DIR_EXP = datetime.datetime.now().isoformat()
	path_experiment = os.path.join(DIR_ROOT, MAIN_DIR_EXP)  
	os.mkdir(path_experiment) 

	os.chdir(path_experiment)
	
	return path_experiment

def run_downsample(edgelength):
	cmd_1 = ["downsample", str(edgelength), "0", IN_PCL_TILE]
	print("Process 1")
	process_1 = run(cmd_1, check=True, stdout=PIPE, universal_newlines=True)
	

def run_getdemslice(resolution, percentil, zmin, zmax, path_experiment):
	cmd_2 = ["getdemslice", str(resolution), str(percentil), str(zmin), str(zmax), get_downsample_file(path_experiment)]
	print("Process 2")
	process_2 = run(cmd_2, check=True, stdout=PIPE, universal_newlines=True)
	

def run_findstems(smooth, dmin, dmax, IN_coords, path_experiment):
	cmd_3 = ["findstems", str(smooth), str(dmin), str(dmax), IN_coords, get_slice_file(path_experiment)]

	print("Process 3")
	try:
		process_3 = run(cmd_3, check=True, stdout=PIPE, universal_newlines=True)
		#print(process_3.stdout)
	except CalledProcessError as error:
		print(f"ERROR: {error}")



def main(args):	
	# ------  ------
	con = sqlite3.connect(db_config)
	cursor = con.cursor()
	id_exp = 0
	previous_d = previous_g = None
	for edgelength, resolution, percentil, zmin, zmax, smooth, dmin, dmax, d, g, f in cursor.execute(query_exp):
		print(f"ID: {id_exp}")
		print(f"START: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
		path_experiment = new_running_dir()
		print(f"FULL PATH: {path_experiment}")
		print(f"downsample(edgelength={edgelength})")
		
		if d != previous_d:
			run_downsample(edgelength)
			
		print(f"getdemslice(resolution={resolution}, percentil={percentil}, zmin={zmin}, zmax={zmax})")
		
		if g != previous_g:
			run_getdemslice(resolution, percentil, zmin, zmax, path_experiment)
			previous_path_experiment = path_experiment
		
		print(f"findstems(smooth={smooth}, dmin={dmin}, dmax={dmax})")
		
		if g != previous_g:
			run_findstems(smooth, dmin, dmax, path_experiment)
		else:
			run_findstems(smooth, dmin, dmax, previous_path_experiment)
		
		print(f"END: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

		
		id_exp += 1
		
	return 0

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))


