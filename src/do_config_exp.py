#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  do_config_exp.py
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

# Experiments setup


import sqlite3
from sys import argv
import numpy as np

file_config = argv[1] # Database file
file_sql = argv[2]    # SQL scheme

# DB Config
con = sqlite3.connect(file_config)

# Initialize config db
sqlTables = open(file_sql).read()
cursor = con.cursor()

cursor.executescript(sqlTables)
con.commit()


#    Experiments Settings
# ---------------------------

downsample = {
        "edgelength": {"min":0.01, "max": 0.1, "step": 0.01},
        "command": "downsample"
}

getdemslice = {
        "resolution": {"min":0.25, "max": 1.5, "step": 0.25},
        "percentil": {"min":0.0, "max": 0.2, "step": 0.1},
        "zmin": {"min":0.0, "max": 0.5, "step": 0.1},
        "zmax": {"min":0.6, "max": 1.5, "step": 0.1},
        "command": "getdemslice"
}

findstems = {
        "smooth": {"min":10, "max":25, "step": 5},
        "dmin": {"min":0.1, "max": 0.5, "step": 0.1},
        "dmax": {"min":0.6, "max": 2.0, "step": 0.1},
        "command": "findstems"
}

def fill_downsample():
	cursor = con.cursor()
	for edgelength in np.arange(downsample["edgelength"]["min"], downsample["edgelength"]["max"], downsample["edgelength"]["step"]):
		cursor.execute("insert into downsample (edgelength) values (?)", (str(edgelength),))
	con.commit()
	print("downsample ... ready")

def fill_getdemslice():
	cursor = con.cursor()
	for resolution in np.arange(getdemslice["resolution"]["min"], getdemslice["resolution"]["max"], getdemslice["resolution"]["step"]):
		for percentil in np.arange(getdemslice["percentil"]["min"], getdemslice["percentil"]["max"], getdemslice["percentil"]["step"]):
			for zmin in np.arange(getdemslice["zmin"]["min"], getdemslice["zmin"]["max"], getdemslice["zmin"]["step"]):
				for zmax in np.arange(getdemslice["zmax"]["min"], getdemslice["zmax"]["max"], getdemslice["zmax"]["step"]):
					cursor.execute("insert into getdemslice (resolution, percentil, zmin, zmax) values (?,?,?,?)", (str(resolution), str(percentil), str(zmin), str(zmax),))
	con.commit()
	print("getdemslice ... ready")

def fill_findstems():
	cursor = con.cursor()
	for smooth in np.arange(findstems["smooth"]["min"], findstems["smooth"]["max"], findstems["smooth"]["step"]):
		for dmin in np.arange(findstems["dmin"]["min"], findstems["dmin"]["max"], findstems["dmin"]["step"]):
			for dmax in np.arange(findstems["dmax"]["min"], findstems["dmax"]["max"], findstems["dmax"]["step"]):
				cursor.execute("insert into findstems (smooth, dmin, dmax) values (?,?,?)", (str(smooth), str(dmin), str(dmax),))
	con.commit()
	print("findstems ... ready")


def main(args):
	fill_downsample()
	fill_getdemslice()
	fill_findstems()
	con.close()
	return 0

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
