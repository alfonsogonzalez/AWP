'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Fundamentals of Orbital Mechanics 3
Ordinary Differential Equations (ODEs) Solvers Introduction

Acceleration, Velocity subplots
for Molniya orbit
Try changing out the orbital parameters and time steps!
'''

# AWP library
from Spacecraft import Spacecraft as SC
import orbit_calculations         as oc

# 3rd party libraries
import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'dark_background' )

import matplotlib
matplotlib.rcParams[ 'lines.linewidth' ] = 2

def rk4_ks( f, t, y, h ):
	'''
	Calculate all RK4 k values
	'''
	k1 = f( t, y )
	k2 = f( t + 0.5 * h, y + 0.5 * k1 * h )
	k3 = f( t + 0.5 * h, y + 0.5 * k2 * h )
	k4 = f( t +       h, y +       k3 * h )
	kt = 1 / 6.0 * ( k1 + 2 * k2 + 2 * k3 + k4 )
	return k1, k2, k3, k4, kt

def rk4_step( f, t, y, h ):
	'''
	Take one RK4 step
	'''
	k1 = f( t, y )
	k2 = f( t + 0.5 * h, y + 0.5 * k1 * h )
	k3 = f( t + 0.5 * h, y + 0.5 * k2 * h )
	k4 = f( t +       h, y +       k3 * h )

	return y + h / 6.0 * ( k1 + 2 * k2 + 2 * k3 + k4 )

'''
Molniya orbital elements
Try changing these elements and seeing how the plots change
'''
raan = 30.0
inc  = 63.4
aop  = 270.0
a    = 26600.0
e    = 0.7
coes = [ a, e, inc, 0.0, aop, raan ]

if __name__ == '__main__':
	h         = 100.0 # try different values of h
	sc_config = {
		'coes' : coes,
		'tspan': '5',
		'dt'   : h
	}	
	sc             = SC( sc_config )
	steps          = sc.states.shape[ 0 ]
	states_rk      = np.zeros( ( steps, 6 ) )
	states_rk[ 0 ] = sc.states[ 0 ][ :6 ]

	for n in range( 1, steps ):
		states_rk[ n ] = rk4_step( oc.two_body_ode, sc.ets[ n ],
			states_rk[ n - 1 ], h )

	# change this to True to see 3D plot of orbit
	if False:
		sc.plot_3d( {
			'colors'   : [ 'c' ],
			'elevation': 13,
			'azimuth'  : -13,
			'legend'   : False, # you are the legend
			'show'     : True
			} )

	accels = np.zeros( ( sc.states.shape[ 0 ], 3 ) )
	rks    = np.zeros( ( sc.states.shape[ 0 ], 5 ) )
	
	accels[ 0 ] = oc.two_body_ode( sc.ets[ 0 ], sc.states[ 0 ] )[ 3: ]
	ks          = rk4_ks( oc.two_body_ode, sc.ets[ 0 ], sc.states[ 0, :6 ], h )
	rks   [ 0 ] = [ k[ 3 ] for k in ks ]

	for n in range( sc.states.shape[ 0 ] - 1 ):
		accels[ n + 1 ] = oc.two_body_ode( sc.ets[ n ], sc.states[ n ] )[ 3: ]
		ks              = rk4_ks( oc.two_body_ode, sc.ets[ n ], states_rk[ n ], h )
		rks   [ n + 1 ] = [ k[ 3 ] for k in ks ]

	fig, ( ax0, ax1 ) = plt.subplots( 2, 1,
		figsize = ( 20, 10 ) )

	ets    = ( sc.ets - sc.ets[ 0 ] ) / 3600.0
	colors = [ 'r', 'g', 'b', 'w', 'm' ]
	labels = [ 'k1', 'k2', 'k3', 'k4', '$k_{wmean}$' ]

	ax0.plot( ets, accels[ :, 0 ], 'r', label = r'$a_x$'   )
	ax0.grid( linestyle = 'dotted' )
	ax0.set_xlim( left = 0, right = ets[ -1 ] )
	ax0.set_ylabel( r'Acceleration $(\dfrac{km}{s^2})$', fontsize = 20 )

	for n in range( 5 ):
		ax0.plot( ets, rks[ :, n ], 'o', markersize = 5,
			color = colors[ n ], label = labels[ n ] )
	ax0.fill_between( ets, rks[ :, 4 ], color = 'm', step = 'mid',
		alpha = 0.7, edgecolor = 'w' )
	ax0.legend( loc = 'upper center' )

	vx_diff = states_rk[ :, 3 ] - sc.states[ :, 3 ]
	ax1.plot( ets, states_rk[ :, 3 ], 'mo' )
	ax1.plot( ets, states_rk[ :, 3 ], 'm--', label = 'RK4' )
	ax1.plot( ets, sc.states[ :, 3 ], 'r', label = 'LSODA' )
	ax1.plot( ets, vx_diff, 'w--', label = 'Diff' )
	ax1.grid( linestyle = 'dotted' )
	ax1.set_xlim( left = 0, right = ets[ -1 ] )
	ax1.set_ylabel( r'Velocity $(\dfrac{km}{s})$', fontsize = 20 )
	ax1.legend( loc = 'upper center' )

	plt.suptitle( f'h = {h} seconds', fontsize = 20 )
	plt.tight_layout()
	plt.show()

	# to save image, comment out plt.show() and uncomment this
	#plt.savefig( path + f'auc_{int(h)}_molniya.png', dpi = 300 )
