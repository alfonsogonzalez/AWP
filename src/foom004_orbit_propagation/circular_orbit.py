'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Fundamentals of Orbital Mechanics 4
Orbital propagation

Circular orbit propagation
'''

# 3rd party libraries
import numpy as np

# AWP library
import orbit_calculations as oc
import ode_tools          as ot
import plotting_tools     as pt
import planetary_data     as pd

if __name__ == '__main__':
	r0_norm     = pd.earth[ 'radius' ] + 450.0          # km
	v0_norm     = ( pd.earth[ 'mu' ] / r0_norm ) ** 0.5 # km / s
	statei      = [ r0_norm, 0, 0, 0, v0_norm, 0 ]
	tspan       = 100.0 * 60.0                          # seconds
	dt          = 100.0                                 # seconds
	steps       = int( tspan / dt )
	ets         = np.zeros( ( steps, 1 ) )
	states      = np.zeros( ( steps, 6 ) )
	states[ 0 ] = statei

	for step in range( steps - 1 ):
		states[ step + 1 ] = ot.rk4_step(
			oc.two_body_ode, ets[ step ], states[ step ], dt )

	pt.plot_orbits( [ states ], { 'show': True } )
