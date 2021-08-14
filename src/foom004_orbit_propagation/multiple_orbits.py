'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Fundamentals of Orbital Mechanics 4
Orbital propagation

GPS, ISS, Geostationary and Molniya orbit propagations
'''

# 3rd party libraries
import numpy as np

# AWP library
import orbit_calculations as oc
import ode_tools          as ot
import plotting_tools     as pt
import planetary_data     as pd

if __name__ == '__main__':
	coes_gps     = [ 26578.0, 1e-3, 55.0, 0, 211.6, 132.3 ]
	coes_iss     = [ 6778.0,  1e-4, 51.6, 0, 0,     0     ]
	coes_geo     = [ 42164.0, 1e-6, 0.0 , 0, 0,     0     ]
	coes_molniya = [ 26600.0, 0.7,  63.4, 0, 270.0, 30.0  ]

	state0_gps          = oc.coes2state( coes_gps )
	state0_iss          = oc.coes2state( coes_iss )
	state0_geo          = oc.coes2state( coes_geo )
	state0_molniya      = oc.coes2state( coes_molniya )
	tspan               = 12.0 * 3600.0
	dt                  = 100.0
	steps               = int( tspan / dt )
	ets                 = np.zeros( ( steps, 1 ) )
	states_gps          = np.zeros( ( steps, 6 ) )
	states_iss          = np.zeros( ( steps, 6 ) )
	states_geo          = np.zeros( ( steps, 6 ) )
	states_molniya      = np.zeros( ( steps, 6 ) )
	states_gps    [ 0 ] = state0_gps
	states_iss    [ 0 ] = state0_iss
	states_geo    [ 0 ] = state0_geo
	states_molniya[ 0 ] = state0_molniya

	for step in range( steps - 1 ):
		states_gps[ step + 1 ]     = ot.rk4_step(
			oc.two_body_ode, ets[ step ], states_gps[ step ], dt )

		states_iss[ step + 1 ]     = ot.rk4_step(
			oc.two_body_ode, ets[ step ], states_iss[ step ], dt )

		states_geo[ step + 1 ]     = ot.rk4_step(
			oc.two_body_ode, ets[ step ], states_geo[ step ], dt )

		states_molniya[ step + 1 ] = ot.rk4_step(
			oc.two_body_ode, ets[ step ], states_molniya[ step ], dt )

	pt.plot_orbits(
		[ states_gps, states_iss, states_geo, states_molniya ],
		{
		'labels'  : [ 'GPS', 'ISS', 'Geostationary', 'Molniya' ],
		'colors'  : [ 'crimson', 'm', 'lime', 'b' ],
		'traj_lws': 2,
		'show'    : True
		} )
