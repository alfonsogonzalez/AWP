'''
Numerical Tools Library
'''

import warnings
import math
import sys
import numpy as np
import spiceypy as spice
from copy import copy

r2d = 180.0 / np.pi
d2r = 1.0  / r2d

frame_transform_dict = {
	3: spice.pxform,
	6: spice.sxform
}

def norm( v ):
	return np.linalg.norm( v )

def normed( v ):
	return v / norm( v )

def frame_transform( arr, tspan, frame_from, frame_to ):
	'''
	Calculate length 3 or 6 vectors to new reference frame
	'''
	transformed = np.zeros( arr.shape )

	for step in range( arr.shape[ 0 ] ):
		matrix = frame_transform_dict[ dim ]( frame_from, frame_to,
						tspan[ step ] )
		transformed[ step ] = np.dot( matrix, arr[ step ] )
	
	return transformed

def bf2latlon( rs ):
	'''
	Calculate latitude / longitude coordinates from body-fixed vectors
	'''

	steps   = rs.shape[ 0 ]
	latlons = np.zeros( rs.shape )

	for step in range( steps ):
		r_norm, lon, lat = spice.reclat( rs[ step ] )
		latlons[ step ] = [ lat * r2d, lon * r2d, r_norm ]

	return latlons

def inert2latlon( rs, frame_from, frame_to, ets ):
	'''
	Calculate latitude / longitude coordinates from inertial vectors
	'''

	bf = frame_transform( rs, ets, frame_from, frame_to )
	return bf2latlon( bf )
