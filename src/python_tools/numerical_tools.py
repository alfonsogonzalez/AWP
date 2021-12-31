'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Numerical Tools Library
'''

# Python standard libraries
import math

# 3rd party libraries
import numpy    as np
import spiceypy as spice

# AWP library
import orbit_calculations as oc
import ode_tools          as ot

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

def Cz( a ):
	'''
	Principal Z axis active rotation matrix by an angle
	'''
	return np.array( [ 
		[ math.cos( a ), -math.sin( a ), 0 ],
		[ math.sin( a ),  math.cos( a ), 0 ],
		[        0,             0,       1 ]
	] )

def newton_root_single( f, fp, x0, args = {} ):
	'''
	Calculate root of single variable function
	using explicit derivative function
	'''
	_args = {
		'tol'        : 1e-10,
		'max_steps'  : 50
	}
	for key in args.keys():
		_args[ key ] = args[ key ]

	delta_x = f( x0, args ) / fp( x0, args )

	for n in range( _args[ 'max_steps' ] ):
		x0     -= delta_x
		delta_x = f( x0, args ) / fp( x0, args )

		if abs( delta_x ) < _args[ 'tol' ]:
			return x0, n

	raise RuntimeError(
		'Newton\'s root solver single variable did not converge.' )

def newton_root_single_fd( f, x0, args = {} ):
	'''
	Calculate root of single variable function using
	finite differences (no explicit derivative function)
	'''
	_args = {
		'tol'        : 1e-10,
		'max_steps'  : 200,
		'diff_method': 'central',
		'diff_step'  : 1e-6
	}
	for key in args.keys():
		_args[ key ] = args[ key ]

	delta_x = f( x0, _args ) /\
				fdiff_cs( f, x0, _args[ 'diff_step' ], _args )

	for n in range( _args[ 'max_steps' ] ):
		x0     -= delta_x
		delta_x = f( x0, _args ) /\
				  fdiff_cs( f, x0, _args[ 'diff_step' ], _args )

		if abs( delta_x ) < _args[ 'tol' ]:
			return x0, n

	raise RuntimeError( 'Newton\'s root solver FD single variable did not converge.' )

def fdiff_cs( f, x, dx, args = {} ):
	'''
	Calculate central finite difference
	of single variable, scalar valued function
	'''
	return ( f( x + dx, args ) - f( x - dx, args ) ) / ( 2 * dx )

def vecs2angle( v0, v1, deg = True ):
	'''
	Calculate angle between 2 vectors
	'''
	angle = math.acos( np.dot( v0, v1 ) / norm( v0 ) / norm( v1 ) )
	if deg:
		angle *= r2d
	return angle

def frame_transform( arr, frame_from, frame_to, ets ):
	'''
	Calculate length 3 or 6 vectors from
	"frame_from" frame to "frame_to" frame using SPICE
	'''
	transformed = np.zeros( arr.shape )
	func        = frame_transform_dict[ arr.shape[ 1 ] ]

	for step in range( arr.shape[ 0 ] ):
		matrix = func( frame_from, frame_to, ets[ step ] )
		transformed[ step ] = np.dot( matrix, arr[ step ] )
	
	return transformed

def cart2lat( rs, frame_from = None, frame_to = None, ets = None, deg = True ):
	'''
	Calculate latitudinal coordinates given cartesian coordinates
	optionally calculating cartesian coordinates in new frame
	before coordinate conversion
	'''
	if frame_from is not None and frame_from != frame_to:
		rs = frame_transform( rs, frame_from, frame_to, ets )

	steps   = rs.shape[ 0 ]
	latlons = np.zeros( ( steps, 3 ) )

	for step in range( steps ):
		'''
		Note: spice.reclat function returns latitudinal
		coordinates in the following order:
		radial, longitude, latitude
		'''
		latlons[ step ] = spice.reclat( rs[ step ] )

	if deg:
		latlons[ :, 1: ] *= r2d

	return latlons

def propagate_ode( ode, state0, tspan, dt, method = 'rk4' ):
	func        = ot.methods[ method ]
	ets         = np.arange( 0, tspan, dt )
	steps       = len( ets )
	states      = np.zeros( ( steps, len( state0 ) ) )
	states[ 0 ] = state0

	for step in range( steps - 1 ):
		states[ step + 1 ] = func(
			ode, ets[ step ], states[ step ], dt )

	return ets, states
