'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Earth solar eclipses 2017 and 2021-2027
'''

import orbit_calculations as oc
import plotting_tools     as pt
import planetary_data     as pd
import spice_data         as sd

import numpy    as np
import spiceypy as spice

if __name__ == '__main__':
	spice.furnsh( sd.leapseconds_kernel )
	spice.furnsh( sd.de432 )
	spice.furnsh( sd.pck00010 )

	dates = [ 
		[ '2017-08-21 16:30', '2017-08-21 20:30' ],
		[ '2021-12-04 07:30', '2021-12-04 08:30' ],
		[ '2023-04-20 02:00', '2023-04-20 06:30' ],
		[ '2024-04-08 16:00', '2024-04-08 20:00' ],
		[ '2026-08-12 16:30', '2026-08-12 18:45' ],
		[ '2027-08-02 08:00', '2027-08-02 12:00' ]
	]
	names   = [ '2017 Great American', '2021-DEC-4', '2023-APR-20' ]
	names  += [ '2024-APR-08', '2026-AUG-12', '2027-AUG-2' ]
	colors  = [ 'r', 'g', 'b', 'm', 'c', 'w' ]
	latlons = []

	for n in range( 6 ):
		et0 = spice.str2et( dates[ n ][ 0 ] )
		etf = spice.str2et( dates[ n ][ 1 ] )
		ets = np.arange( et0, etf, 20 )
		latlons.append(
			oc.calc_solar_eclipse_array( ets, pd.moon, pd.earth )
		)

	pt.plot_groundtracks( latlons, {
		'colors'  : colors,
		'labels'  : names,
		'show'    : True
		} )

