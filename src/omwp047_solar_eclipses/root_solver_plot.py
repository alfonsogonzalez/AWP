'''
Visualizations for penumbra edge cases
'''

import orbit_calculations as oc
import numerical_tools    as nt
import spice_data         as sd

import numpy             as np
import spiceypy          as spice
import matplotlib.pyplot as plt
plt.style.use( 'dark_background' )

if __name__ == '__main__':
	spice.furnsh( sd.leapseconds_kernel )
	spice.furnsh( sd.de432 )
	spice.furnsh( sd.pck00010 )

	et           = spice.str2et( '2017-08-21 18:30' )
	r_sun2moon   = spice.spkpos( '301', et, 'J2000', 'LT', 'SUN' )[ 0 ]
	r_moon2earth = spice.spkpos( '399', et, 'J2000', 'LT', '301' )[ 0 ]
	delta_ps     = nt.norm( r_sun2moon )
	s_hat        = r_sun2moon / delta_ps
	proj_scalar  = np.dot( r_moon2earth, s_hat )
	proj         = proj_scalar * s_hat
	rej_norm     = nt.norm( r_moon2earth - proj )
	args         = { 'r': r_moon2earth, 's_hat': s_hat, 'radius': 6378.0 }
	sigma        = nt.newton_root_single_fd( oc.eclipse_root_func,
					proj_scalar / 2.0, args )[ 0 ]
	sigmas       = np.arange( sigma - 10000, sigma + 15000, 10 )
	n_sigmas     = len( sigmas )
	vals         = np.zeros( n_sigmas )

	for n in range( n_sigmas ):
		vals[ n ] = oc.eclipse_root_func( sigmas[ n ], args )

	plt.figure( figsize = ( 16, 8 ) )
	plt.plot( sigmas, vals, 'm', lw = 3 )
	plt.plot( sigma, 0, 'r*', markersize = 15 )
	plt.vlines( sigma, -4000, 10000, 'r', lw = 2, linestyle = 'dotted' )
	plt.vlines( proj_scalar, -4000, 10000, 'c', lw = 2, linestyle = 'dotted' )
	plt.hlines( 0, sigmas[ 0 ], sigmas[ -1 ], 'w', lw = 2 )
	plt.grid( linestyle = 'dotted' )
	plt.xlim( [ sigmas[ 0 ], sigmas[ -1 ] ] )
	plt.ylim( [ -4000, 10000 ] )
	plt.xlabel( r'$\sigma$', fontsize = 20 )
	plt.ylabel( r'$f(\sigma)$', fontsize = 20 )
	plt.show()
