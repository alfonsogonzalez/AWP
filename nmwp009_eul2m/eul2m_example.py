'''
Print Symbolic Euler Angle Rotation Matrix
'''

# built-in Python library
from sys import path
path.append( '/home/alfonso/AWP/python_tools' )

# personal libraries
import plotting_tools as pt

# 3rd party library
import spiceypy as spice

d2r = 3.14159 / 180.0
fn  = 'frames.png'

if __name__ == '__main__':

	raan   =  30.0  * d2r
	inc    =  63.4  * d2r
	aop    =  270.0 * d2r
	eul313 = spice.eul2m( aop, inc, raan, 3, 1, 3 )
	frames = [ eul313, eul313.T ]

	print( 'eul2m' )
	print( eul313 )
	print()
	print( 'transpose' )
	print( eul313.T )

	config = {
		'frame_colors': [ 'm', 'c' ],
		'frame_labels': [ 'eul2m', 'Transpose' ],
		'elevation'   : 12,
		'azimuth'     : -19,
		#'filename'    : fn
		'show': True
	}

	pt.plot_reference_frames( frames, config )


