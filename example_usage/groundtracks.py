'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Propagate orbits with Spacecraft class and plot resulting
groundtracks
'''

# 3rd party libraries
import spiceypy as spice

# AWP libraries
from Spacecraft import Spacecraft as SC
import plotting_tools as pt
import spice_data     as sd
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
		'tspan': '3',
		'dt'   : 20.0
	}
	for coes in [ coes0, coes1, coes2, coes3 ]:
		sc_config[ 'coes' ] = coes
		sc = SC( sc_config )
		sc.calc_latlons()
		latlons.append( sc.latlons )

	pt.plot_groundtracks( latlons, 
		{
		'labels': [ 'LEO', 'Geosynchronous', 'Sun Sync', 'Retrograde' ],
		'show'  : True
		} )