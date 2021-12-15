'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Low Earth Orbit (LEO) Spacecraft simulation with
eclipse calculations

NOTE script will error if leo.bsp already exists
'''

# AWP library
from Spacecraft import Spacecraft as SC
import spice_data  as sd
import spice_tools as st

# 3rd party libraries
import spiceypy as spice

if __name__ == '__main__':
	spice.furnsh( sd.leapseconds_kernel )
	spice.furnsh( sd.de432 )
	spice.furnsh( sd.pck00010 )

	sc = SC( {
		'date0': '2021-03-03 22:10:35 TDB',
		'coes' : [ 7480.0, 0.09, 5.5, 6.26, 5.95, 0.2 ],
		'tspan': '40',
		} )

	st.write_bsp( sc.ets, sc.states[ :, :6 ],
			{ 'bsp_fn': 'leo.bsp' } )
	spice.furnsh( 'leo.bsp' )

	et0  = spice.str2et( '2021-03-03 22:10:40 TDB' )
	etf  = spice.str2et( '2021-03-04 TDB' )

	timecell = spice.utils.support_types.SPICEDOUBLE_CELL( 2 )
	spice.appndd( et0, timecell )
	spice.appndd( etf, timecell )

	cell = spice.gfoclt( 'ANY', '399', 'ELLIPSOID', 'IAU_EARTH',
		'10', 'ELLIPSOID', 'IAU_SUN', 'LT', '-999', 120.0, timecell )
	ets_SPICE = spice.wnfetd( cell, 0 )
	cal0      = spice.et2utc( ets_SPICE[ 0 ], 'C', 1 )
	cal1      = spice.et2utc( ets_SPICE[ 1 ], 'C', 1 )
	print( '\n*** SPICE RESULTS ***' )
	print( f'{cal0} --> {cal1}')

	sc.plot_3d()
	sc.calc_eclipses( vv = True )

	sc.plot_eclipse_array( {
		'time_unit': 'seconds',
		'show'     : True
	} )
