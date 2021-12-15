'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Jupiter solar eclipses

NOTE: If you want to run this script, you'll need to
download and spice.furnsh jup365.bsp from here:
https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/satellites/
'''

import orbit_calculations as oc
import plotting_tools as pt
import planetary_data  as pd
import spice_data as sd

import numpy as np
import spiceypy as spice

if __name__ == '__main__':
	spice.furnsh( sd.leapseconds_kernel )
	spice.furnsh( sd.de432 )
	spice.furnsh( sd.pck00010 )

	# Add your own local path to jup365.bsp here
	#spice.furnsh( '/home/alfonso/AWP/spice/spk/jup365.bsp' )
	pd.jupiter[ 'SPICE_ID' ] = 599
 
	names   = [ '1996 Io', '2021 Europa', '2021 Ganymede', '2021 Callisto' ]
	colors  = [ 'r', 'b', 'm', 'c' ]
	latlons = []

	et0 = spice.str2et( '1996-07-24 18:30' )
	etf = spice.str2et( '1996-07-24 21:30' )
	ets = np.arange( et0, etf, 30 )
	latlons.append(
		oc.calc_solar_eclipse_array( ets, pd.io, pd.jupiter )
	)

	et0 = spice.str2et( '2021-08-15 09:00' )
	etf = spice.str2et( '2021-08-15 18:00' )
	ets = np.arange( et0, etf, 30 )
	latlons.append(
		oc.calc_solar_eclipse_array( ets, pd.europa, pd.jupiter )
	)
	latlons.append(
		oc.calc_solar_eclipse_array( ets, pd.ganymede, pd.jupiter )
	)
	latlons.append(
		oc.calc_solar_eclipse_array( ets, pd.callisto, pd.jupiter )
	)	

	pt.plot_groundtracks( latlons, {
		'colors'      : colors,
		'labels'      : names,
		'surface_body': 'jupiter',
		'city_names'  : [],
		'show'        : True
		} )

