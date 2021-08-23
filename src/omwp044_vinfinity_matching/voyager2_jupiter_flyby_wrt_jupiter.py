'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

3Blue1Brown's Summer of Math Exposition video entry
and Orbital Mechanics with Python 44
Gravity Assist Design via V-Infinity Matching to Explore
Our Solar System

Create 3D plot and orbital states plot of Voyager 2 flyby
with respect to Jupiter

*********** NOTE ************
If you'd like to run this script, you must
run it from this directory so that the path to the
Voyager 2 SPICE kernel is correct. Or you can change the path
to fit your needs
'''

# 3rd party libraries
import spiceypy as spice
import numpy    as np

# AWP library
import spice_tools    as st
import plotting_tools as pt
import planetary_data as pd
import spice_data     as sd
from numerical_tools import norm

if __name__ == '__main__':
	spice.furnsh( sd.leapseconds_kernel )
	spice.furnsh( 'voyager2_jupiter_flyby.bsp' )

	et     = spice.str2et( '1979-07-09 TDB' )
	dt     = 20 * 24 * 3600.0
	ets    = np.arange( et - dt, et + dt, 5000.0 )
	states = st.calc_ephemeris( -32, ets, 'ECLIPJ2000', 5 )

	pt.plot_orbits( [ states[ :, :3 ] ],
	{
	'labels'   : [ 'Voyager 2' ],
	'colors'   : [ 'm' ],
	'cb_radius': pd.jupiter[ 'radius' ],
	'cb_cmap'  : 'Oranges',
	'dist_unit': 'JR',
	'azimuth'  : -57,
	'elevation':  15,
	'axes_mag' : 0.5,
	'show'     : True
	} )

	hline = { 'val': norm( states[ 0, 3: ] ), 'color': 'm' }
	pt.plot_velocities( ets, states[ :, 3: ], 
		{
		'time_unit': 'hours',
		'hlines'   : [ hline ],
		'show'     : True
		} )
