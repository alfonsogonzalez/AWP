'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Propagate orbits with Spacecraft class and plot resulting
groundtracks
'''

# 3rd party libraries
from numpy import arange
import spiceypy as spice

# AWP libraries
from Spacecraft import Spacecraft as SC
import numerical_tools as nt
import plotting_tools  as pt
import spice_data      as sd
from planetary_data import earth

if __name__ == '__main__':
	spice.furnsh( sd.pck00010 )

	ER        = earth[ 'radius' ]
	coes0     = [ ER + 400,   0.01, 45.0,  0, 0.0, 0 ] # LEO
	coes1     = [ 42164.0,    0.2,  55.0,  0, -80, 0 ] # geosync
	coes2     = [ ER + 890.0, 0.0,  99.0,  0,   0, 0 ] # sunsync
	coes3     = [ ER + 500,   0.01, 135.0, 0,   0, 0 ] # retrograde
	latlons   = []
	sc_config = {
		'tspan'       : '3',
		'dense_output': True
	}
	for coes in [ coes0, coes1, coes2, coes3 ]:
		sc_config[ 'coes' ] = coes
		sc      = SC( sc_config )
		ets     = arange( sc.ets[ 0 ], sc.ets[ -1 ], 15.0 )
		rs      = sc.ode_sol.sol( ets ).T[ :, :3 ]

		latlons.append( nt.cart2lat( rs, 'J2000', 'IAU_EARTH', ets ) )

	pt.plot_groundtracks( latlons, 
		{
		'labels': [ 'LEO', 'Geosynchronous', 'Sun Sync', 'Retrograde' ],
		'show'  : True
		} )