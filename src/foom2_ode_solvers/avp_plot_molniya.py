'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Fundamentals of Orbital Mechanics 2
Ordinary Differential Equations (ODEs) Solvers

Acceleration, Velocity and Position subplots script
for Molniya orbit
Try changing out the orbital parameters!
'''

from Spacecraft import Spacecraft as SC
import orbit_calculations as oc

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'dark_background' )
import matplotlib
matplotlib.rcParams[ 'lines.linewidth' ] = 2

# Molniya orbital elements
raan = 30.0
inc  = 63.4
aop  = 270.0
a    = 26600.0
e    = 0.7
coes = [ a, e, inc, 0.0, aop, raan ]

sc_config = {
	'coes' : coes,
	'tspan': '2.5',
	'dt'   : 100.0
}

if __name__ == '__main__':
	sc = SC( sc_config )

	sc.plot_3d( {
		'colors'   : [ 'c' ],
		'elevation': 13,
		'azimuth'  : -13,
		'legend'   : False, # you are the legend
		'show'     : True
		} )

	accels = np.zeros( ( sc.states.shape[ 0 ], 3 ) )
	
	for n in range( sc.states.shape[ 0 ] ):
		accels[ n ] = oc.two_body_ode( sc.ets[ n ], sc.states[ n ] )[ 3: ]

	rnorms = np.linalg.norm( sc.states[ :,  :3 ], axis = 1 )
	vnorms = np.linalg.norm( sc.states[ :, 3:6 ], axis = 1 )
	anorms = np.linalg.norm( accels, axis = 1 )

	fig, ( ax0, ax1, ax2 ) = plt.subplots( 3, 1,
		figsize = ( 20, 10 ) )

	ets = ( sc.ets - sc.ets[ 0 ] ) / 3600.0

	ax0.plot( ets, accels[ :, 0 ], 'r', label = r'$a_x$'   )
	ax0.plot( ets, accels[ :, 1 ], 'g', label = r'$a_y$'   )
	ax0.plot( ets, accels[ :, 2 ], 'b', label = r'$a_z$'   )
	ax0.plot( ets, anorms        , 'm', label = r'$Norms$' )
	ax0.grid( linestyle = 'dotted' )
	ax0.set_xlim( left = 0, right = 30 )
	ax0.set_ylabel( r'Acceleration $(\dfrac{km}{s^2})$', fontsize = 20 )
	ax0.legend( loc = 'upper center' )

	ax1.plot( ets, sc.states[ :, 3 ], 'r', label = r'$v_x$'   )
	ax1.plot( ets, sc.states[ :, 4 ], 'g', label = r'$v_y$'   )
	ax1.plot( ets, sc.states[ :, 5 ], 'b', label = r'$v_z$'   )
	ax1.plot( ets, vnorms           , 'm', label = r'$Norms$' )
	ax1.grid( linestyle = 'dotted' )
	ax1.set_xlim( left = 0, right = 30 )
	ax1.set_ylabel( r'Velocity $(\dfrac{km}{s})$', fontsize = 20 )
	ax1.legend( loc = 'upper center' )

	ax2.plot( ets, sc.states[ :, 0 ], 'r', label = r'$r_x$'   )
	ax2.plot( ets, sc.states[ :, 1 ], 'g', label = r'$r_y$'   )
	ax2.plot( ets, sc.states[ :, 2 ], 'b', label = r'$r_z$'   )
	ax2.plot( ets, rnorms,            'm', label = r'$Norms$' )
	ax2.grid( linestyle = 'dotted' )
	ax2.set_xlim( left = 0, right = 30 )
	ax2.set_ylabel( r'Position $(km)$', fontsize = 20 )
	ax2.set_xlabel( 'Time (hours)' )
	ax2.legend( loc = 'upper right' )

	plt.tight_layout()
	plt.show()
