'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Fundamentals of Orbital Mechanics 4
Orbital propagation

Many orbits with equal initial position vectors
to demonstrate that position alone does not fully
describe an orbit
'''

# 3rd party libraries
import numpy as np

# AWP library
from Spacecraft import Spacecraft as SC
import orbit_calculations as oc
import ode_tools          as ot
import plotting_tools     as pt
import planetary_data     as pd

if __name__ == '__main__':
	r0      = pd.earth[ 'radius' ] + 1000.0
	v0_circ = ( pd.earth[ 'mu' ] / r0 ) ** 0.5
 
	state0_sc0 = [ r0, 0, 0, 0, v0_circ, 0.0 ]
	state0_sc1 = [ r0, 0, 0, 2.0, 9.0, 0.0 ]
	state0_sc2 = [ r0, 0, 0, 1.0, 0.0, 8.0 ]
	state0_sc3 = [ r0, 0, 0, 1.0, 6.0, 6.0 ]

	states0   = [ state0_sc0, state0_sc1, state0_sc2, state0_sc3 ]
	rs        = []
	sc_config = {
		'tspan': '1'
	}

	for state0 in states0:
		sc_config[ 'orbit_state' ] = state0
		rs.append( SC( sc_config ).states[ :, :3 ] )

	pt.plot_orbits( rs,
		{
		'labels'   : range( 4 ),
		'colors'   : [ 'C3', 'm', 'c', 'lime' ],
		'traj_lws' : 2,
		'azimuth'  : -32,
		'elevation': 70,
		'show'     : True
		} )
