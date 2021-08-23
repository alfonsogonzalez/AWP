'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

3Blue1Brown's Summer of Math Exposition video entry
and Orbital Mechanics with Python 44
Gravity Assist Design via V-Infinity Matching to Explore
Our Solar System

V-infinity matching root solving problem for Venus flyby
'''

# 3rd party libraries
import spiceypy          as spice
import numpy             as np
import matplotlib.pyplot as plt
plt.style.use( 'dark_background' )
plt.rcParams.update( { 'font.size': 13 } )

# AWP library
import orbit_calculations as oc
import numerical_tools    as nt
import planetary_data     as pd
from EVME_1963 import calc_EVME_1963

if __name__ == '__main__':
	itvim        = calc_EVME_1963()
	seq1         = itvim.seq[ 1 ]
	v_arrive     = seq1[ 'state_sc_arrive' ][ 3: ]
	state_venus  = spice.spkgeo( 2, seq1[ 'et' ], 'ECLIPJ2000', 0 )[ 0 ]
	vinf         = nt.norm( v_arrive - state_venus[ 3: ] )
	span         = 60 * 24 * 3600.0
	dt           = 1  * 24 * 3600.0
	tofs         = np.arange( seq1[ 'tof' ] - span, seq1[ 'tof' ] + span, dt )
	n_tofs       = len( tofs )
	vinfs        = np.zeros( n_tofs )
	args = {
		'planet1_ID'    : 4,
		'center_ID'     : 0,
		'et0'           : seq1[ 'et' ],
		'frame'         : 'ECLIPJ2000',
		'state0_planet0': state_venus,
		'mu'            : pd.sun[ 'mu' ],
		'tm'            : 1,
		'vinf'          : vinf
	}

	for n in range( n_tofs ):
		vinfs[ n ] = oc.calc_vinfinity( tofs[ n ], args )

	tofs *= 1 / ( 3600.0 * 24 )
	plt.figure( figsize = ( 12, 8 ) )
	plt.plot( tofs, vinfs, 'm', linewidth = 2 )
	plt.plot( tofs[ 60 ], vinfs[ 60 ], '*', color = 'lime', markersize = 20 )
	plt.hlines( 0.0, tofs[ 0 ], tofs[ -1 ], color = 'c' )
	plt.grid( linestyle = 'dotted' )
	plt.xlim( [ 75, 200 ] )
	plt.xlabel( 'Time of Flight (days)', size = 15 )
	plt.ylabel( r'$\Delta v_{\infty}$ $(\dfrac{km}{s})$', size = 25, color = 'm' )
	plt.show()
