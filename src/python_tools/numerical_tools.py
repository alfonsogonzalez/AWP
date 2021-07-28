'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Numerical Tools Library
'''

import numpy as np
import spiceypy as spice

r2d     = 180.0 / np.pi
d2r     = 1.0  / r2d
sec2day = 1.0 / 3600.0 / 24.0
fps2kms = 0.0003048
mi2km   = 1.60934

frame_transform_dict = {
	3: spice.pxform,
	6: spice.sxform
}

def norm( v ):
	return np.linalg.norm( v )

def normed( v ):
	return v / np.linalg.norm( v )

def frame_transform( arr, ets, frame_from, frame_to ):
	'''
	Calculate length 3 or 6 vectors in frame_from
	to frame_to reference frame
	'''
	transformed = np.zeros( arr.shape )
	dim         = arr.shape[ 1 ]

	for step in range( arr.shape[ 0 ] ):
		matrix = frame_transform_dict[ dim ](
			frame_from, frame_to, ets[ step ] )
		transformed[ step ] = np.dot( matrix, arr[ step ] )
	
	return transformed

def bf2latlon( rs ):
	'''
	Calculate latitude / longitude coordinates
	from body-fixed vectors
	'''

	steps   = rs.shape[ 0 ]
	latlons = np.zeros( rs.shape )

	for step in range( steps ):
		r_norm, lon, lat = spice.reclat( rs[ step ] )
		latlons[ step ]  = [ lat * r2d, lon * r2d, r_norm ]

	return latlons

def inert2latlon( rs, frame_from, frame_to, ets ):
	'''
	Calculate latitude / longitude coordinates
	from inertial vectors
	'''

	bf = frame_transform( rs, ets, frame_from, frame_to )
	return bf2latlon( bf )
