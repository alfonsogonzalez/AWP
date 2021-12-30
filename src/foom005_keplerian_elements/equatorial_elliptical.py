'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Fundamentals of Orbital Mechanics 5
Introduction to Keplerian Orbital Elements

Create equatorial, elliptical orbit SPICE BSP kernel
and true anomaly vs time plot
'''

# 3rd party library
import numpy             as np
import matplotlib.pyplot as plt
plt.style.use( 'dark_background' )

# AWP library
import numerical_tools    as nt
import orbit_calculations as oc
import plotting_tools     as pt


if __name__ == '__main__':
	state0 = [ 7500.0, 0, 0, 0, 9.0, 0 ]	
	tspan  = 5 * 24 * 3600.0
	ets, states = nt.propagate_ode(
		oc.two_body_ode, state0, tspan, 30.0 )

	pt.plot_orbits( [ states[ :, :3 ] ], {
		'colors'  : [ 'm' ],
		'traj_lws': 2,
		'show'    : True
	} )

	n_states = 1350
	tas      = np.zeros( n_states )
	for n in range( n_states ):
		tas[ n ] = oc.state2coes( states[ n ] )[ 3 ]

	plt.figure( figsize = ( 14, 8 ) )
	plt.plot( ets[ :n_states ] / 3600.0, tas, 'm', linewidth = 3 )
	plt.grid( linestyle = 'dotted' )
	plt.yticks( range( 0, 390, 30 ), fontsize = 15 )
	plt.xticks( fontsize = 15 )
	plt.ylim( [ 0, 360 ] )
	plt.xlabel( 'Time (hours)', fontsize = 15 )
	plt.ylabel( r'True Anomaly $\Theta^{\circ}$', fontsize = 15 )
	plt.show()

	'''
	This part is outside the scope of this lesson, but for those
	who are curious this is how to write the trajectory to a
	SPICE .bsp kernel to then use in Cosmographia
	In general, it is bad practice to have imports in this
	part of the code.
	'''
	if False:
		import spiceypy     as spice
		import spice_data   as sd
		import spice_tools  as st
		spice.furnsh( sd.leapseconds_kernel )

		ets += spice.str2et( '2021-12-26' )

		st.write_bsp( ets, states, {
			'bsp_fn': fp + 'equatorial-elliptical.bsp'
		} )
