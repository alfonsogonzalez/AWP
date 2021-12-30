'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Fundamentals of Orbital Mechanics 5
Introduction to Keplerian Orbital Elements

Create orbit SPICE BSP kernel for plots comparing
orbital inclination
'''

# 3rd party libraries
import spiceypy as spice

# AWP library
import numerical_tools    as nt
import orbit_calculations as oc
import plotting_tools     as pt
import spice_data         as sd

if __name__ == '__main__':
	spice.furnsh( sd.leapseconds_kernel )
	spice.furnsh( sd.pck00010 )

	coes_list   = []
	states_list = []
	tspan       = 24 * 3600.0
	dt          = 10.0

	coes_list.append( [ 8000.0, 0.2, 0,   0, 0, 0 ] )
	coes_list.append( [ 8000.0, 0.2, 45,  0, 0, 0 ] )
	coes_list.append( [ 8000.0, 0.2, 75,  0, 0, 0 ] )
	coes_list.append( [ 8000.0, 0.2, 100, 0, 0, 0 ] )

	for coes in coes_list:
		state0      = oc.coes2state( coes )
		ets, states = nt.propagate_ode(
			oc.two_body_ode, state0, tspan, dt )
		states_list.append( states )

	pt.plot_orbits( states_list, {
		'labels'  : [ '0', '45', '75', '100' ],
		'colors'  : [ 'crimson', 'lime', 'c', 'm' ],
		'traj_lws': 2,
		'show'    : True
	} )

	ets    += spice.str2et( '2021-12-26' )
	latlons = []
	for states in states_list:
		latlons.append( nt.cart2lat(
			states[ :1000, :3 ], 'J2000', 'IAU_EARTH', ets ) )

	pt.plot_groundtracks( latlons, {
		'labels'  : [ '0', '45', '75', '100' ],
		'colors'  : [ 'crimson', 'lime', 'c', 'm' ],
		'show'    : True
	} )

	'''
	This part is outside the scope of this lesson, but for those
	who are curious this is how to write the trajectory to a
	SPICE .bsp kernel to then use in Cosmographia
	In general, it is bad practice to have imports in this
	part of the code, so don't try this at home!
	'''
	if False:
		import spice_tools  as st
		spice.furnsh( sd.leapseconds_kernel )


		st.write_bsp( ets, states_list[ 0 ], {
			'bsp_fn': fp + 'inclinations.bsp'
		} )

		for n in [ 1, 2, 3 ]:
			st.write_bsp( ets, states_list[ n ], {
				'bsp_fn'  : fp + 'inclinations.bsp',
				'spice_id': -999 + n,
				'new'     : False
			} )
