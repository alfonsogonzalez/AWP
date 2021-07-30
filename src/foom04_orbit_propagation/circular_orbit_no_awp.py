'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Fundamentals of Orbital Mechanics 4
Orbital propagation

Circular orbit propagation with no AWP dependencies
'''

# 3rd party libraries
import numpy as np

# AWP library
import plotting_tools as pt

earth_radius = 6378.0 # km
earth_mu     = 3.9860043543609598E+05 # km^3 / s^2

def two_body_ode( t, state ):
	r = state[ :3 ]
	a = -earth_mu * r / np.linalg.norm( r ) ** 3

	return np.array( [ state[ 3 ], state[ 4 ], state[ 5 ],
			 a[ 0 ], a[ 1 ], a[ 2 ] ] )

def rk4_step( f, t, y, h ):
	'''
	Calculate one RK4 step
	'''
	k1 = f( t, y )
	k2 = f( t + 0.5 * h, y + 0.5 * k1 * h )
	k3 = f( t + 0.5 * h, y + 0.5 * k2 * h )
	k4 = f( t +       h, y +       k3 * h )

	return y + h / 6.0 * ( k1 + 2 * k2 + 2 * k3 + k4 )

if __name__ == '__main__':
	r0_norm     = earth_radius + 450.0             # km
	v0_norm     = ( earth_mu / r0_norm ) ** 0.5    # km / s
	statei      = [ r0_norm, 0, 0, 0, v0_norm, 0 ]
	tspan       = 100.0 * 60.0                     # seconds
	dt          = 100.0                            # seconds
	steps       = int( tspan / dt )
	ets         = np.zeros( ( steps, 1 ) )
	states      = np.zeros( ( steps, 6 ) )
	states[ 0 ] = statei

	for step in range( steps - 1 ):
		states[ step + 1 ] = rk4_step(
			two_body_ode, ets[ step ], states[ step ], dt )

	print( states )
	pt.plot_orbits( [ states ], { 'show': True } )
