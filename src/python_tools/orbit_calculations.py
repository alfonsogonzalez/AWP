'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Orbit Calculations Library
'''

# 3rd party libraries
import numpy as np
import math
import spiceypy as spice

# AWP library
import numerical_tools as nt
import lamberts_tools  as lt
import planetary_data  as pd

def esc_v( r, mu = pd.earth[ 'mu' ] ):
	'''
	Calculate escape velocity at given radial distance from body
	'''
	return math.sqrt( 2 * mu / r )
 
def state2coes( state, args = {} ):
	_args = {
		'et'        : 0,
		'mu'        : pd.earth[ 'mu' ],
		'deg'       : True,
		'print_coes': False
	}
	for key in args.keys():
		_args[ key ] = args[ key ]

	rp,e,i,raan,aop,ma,t0,mu,ta,a,T = spice.oscltx( 
		state, _args[ 'et' ], _args[ 'mu' ] )

	if _args[ 'deg' ]:
		i    *= nt.r2d
		ta   *= nt.r2d
		aop  *= nt.r2d
		raan *= nt.r2d

	if _args[ 'print_coes' ]:
		print( 'a'   , a    )
		print( 'e'   , e    )
		print( 'i'   , i    )
		print( 'RAAN', raan )
		print( 'AOP' , aop  )
		print( 'TA'  , ta   )
		print()

	return [ a, e, i, ta, aop, raan ]

def state2period( state, mu = pd.earth['mu'] ):

	# specific mechanical energy
	epsilon = nt.norm( state[ 3:6 ] ) ** 2 / 2.0 - mu / nt.norm( state[ :3 ] )

	# semi major axis
	a = -mu / ( 2.0 * epsilon )

	# period
	return 2 * math.pi * math.sqrt( a ** 3 / mu )

def coes2state( coes, mu = pd.earth[ 'mu' ], deg = True ):
	a, e, i, ta, aop, raan = coes
	if deg:
		i    *= nt.d2r
		ta   *= nt.d2r
		aop  *= nt.d2r
		raan *= nt.d2r

	rp = a * ( 1 - e )

	return spice.conics( [ rp, e, i, raan, aop, ta, 0, mu], 0 )

def state2ap( state, mu = pd.earth[ 'mu' ] ):
	h       = nt.norm( np.cross( state[ :3 ], state[ 3: ] ) )
	epsilon = nt.norm( state[ 3: ] ) ** 2 / 2.0 - mu / nt.norm( state[ :3 ] )
	e       = math.sqrt( 2 * epsilon * h ** 2 / mu ** 2 + 1 )
	a       = h ** 2 / mu / ( 1 - e ** 2 )
	ra      = a * ( 1 + e )
	rp      = a * ( 1 - e )
	return  ra, rp

def two_body_ode( t, state, mu = pd.earth[ 'mu' ] ):
	# state = [ rx, ry, rz, vx, vy, vz ]

	r = state[ :3 ]
	a = -mu * r / np.linalg.norm( r ) ** 3

	return np.array( [ state[ 3 ], state[ 4 ], state[ 5 ],
			 a[ 0 ], a[ 1 ], a[ 2 ] ] )

def calc_close_approach( turn_angle, v_inf, mu = pd.sun[ 'mu' ] ):
	'''
	Calculate periapsis distance in flyby trajectory
	'''
	return mu * ( 1 / math.sin( turn_angle ) - 1 ) / v_inf ** 2

def calc_vinfinity( tof, args ):

	r1_planet1 = spice.spkgps( args[ 'planet1_ID' ],
		args[ 'et0' ] + tof, args[ 'frame' ], args[ 'center_ID' ] )[ 0 ]

	v0_sc_depart, v1_sc_arrive = lt.lamberts_universal_variables(
		args[ 'state0_planet0' ][ :3 ], r1_planet1, tof,
		{ 'mu': args[ 'mu' ], 'tm': args[ 'tm' ] } )

	vinf = nt.norm( v0_sc_depart - args[ 'state0_planet0' ][ 3: ] )
	return vinf - args[ 'vinf' ]

def vinfinity_match( planet0, planet1, v0_sc, et0, tof0, args = {} ):
	'''
	Given an incoming v-infinity vector to planet0, calculate the
	outgoing v-infinity vector that will arrive at planet1 after
	time of flight (tof) where the incoming and outgoing v-infinity
	vectors have equal magnitude
	'''
	_args = {
		'et0'           : et0,
		'planet1_ID'    : planet1,
		'frame'         : 'ECLIPJ2000',
		'center_ID'     : 0,
		'mu'            : pd.sun[ 'mu' ],
		'tm'            : 1,
		'diff_step'     : 1e-3,
		'tol'           : 1e-4
	}
	for key in args.keys():
		_args[ key ] = args[ key ]

	_args[ 'state0_planet0' ] = spice.spkgeo( planet0, et0,
		_args[ 'frame' ], _args[ 'center_ID' ] )[ 0 ]

	_args[ 'vinf' ] = nt.norm( v0_sc - _args[ 'state0_planet0' ][ 3: ] )

	tof, steps = nt.newton_root_single_fd(
		calc_vinfinity, tof0, _args )

	r1_planet1 = spice.spkgps( planet1, et0 + tof,
		_args[ 'frame' ], _args[ 'center_ID' ] )[ 0 ]

	v0_sc_depart, v1_sc_arrive = lt.lamberts_universal_variables(
		_args[ 'state0_planet0' ][ :3 ], r1_planet1, tof,
		{ 'mu': _args[ 'mu' ], 'tm': _args[ 'tm' ] } )

	return tof, v0_sc_depart, v1_sc_arrive
