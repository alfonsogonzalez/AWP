'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Lambert Solvers Unit Tests
'''

# 3rd party libraries
import pytest
import numpy as np
import spiceypy as spice

# AWP library
from Spacecraft import Spacecraft
import lamberts_tools as lt
import spice_tools    as st
import planetary_data as pd
import spice_data     as sd
import plotting_tools as pt

# Treat all warnings as errors
pytestmark = pytest.mark.filterwarnings( 'error' )

def test_stumpffs_negative_psi_expect_throw():
	with pytest.raises( ValueError ):
		lt.C2( -1.0 )
	
	with pytest.raises( ValueError ):
		lt.C3( -1.0 )

def test_lambert_uv_earth_to_venus( plot = False ):
	spice.furnsh( sd.leapseconds_kernel )
	spice.furnsh( sd.de432 )

	frame        = 'ECLIPJ2000'
	observer     = 0
	date0        = '2005-12-01'
	datef        = '2006-03-01'
	departure    = spice.utc2et( date0 )
	arrival      = spice.utc2et( datef )
	dt           = arrival - departure
	state0_earth = spice.spkgeo( 399, departure, frame, observer )[ 0 ]
	statef_venus = spice.spkgeo( 2,   arrival,   frame, observer )[ 0 ]
	v0_sc, v1_sc = lt.lamberts_universal_variables(
		state0_earth[ :3 ], statef_venus[ :3 ], dt,
		{ 'mu': pd.sun[ 'mu' ], 'tm': 1 } )
		
	state0_sc = np.concatenate( ( state0_earth[ :3 ], v0_sc ) )
	sc        = Spacecraft( {
		'cb'         : pd.sun,
		'date0'      : date0,
		'tspan'      : dt,
		'dt'         : 500.0,
		'frame'      : frame,
		'orbit_state': state0_sc,
		'atol'       : 1e-9,
		'rtol'       : 1e-9,
	} )
	rdiff = np.linalg.norm( sc.states[ -1, :3 ] - statef_venus[ :3 ] )

	assert np.all( sc.states[ 0, :3 ] == state0_earth[ :3 ] )
	assert pytest.approx( rdiff, abs = 2.0e4 ) == 0.0

	if plot:
		ets          = np.arange( departure, arrival, 5000 )
		states_earth = st.calc_ephemeris( 399, ets, frame, observer )
		states_venus = st.calc_ephemeris( 2,   ets, frame, observer )

		pt.plot_orbits(
			[
			states_earth[ :, :3 ],
			states_venus[ :, :3 ],
			sc.states   [ :, :3 ]
			],
			{
				'cb_radius': pd.sun[ 'radius' ] * 10,
				'cb_cmap'  : 'spring',
				'dist_unit': 'AU',
				'labels'   : [ 'Earth', 'Venus', 'Spacecraft' ],
				'colors'   : [ 'b', 'gold', 'm' ],
				'azimuth'  : 35,
				'elevation': 25,
				'axes_mag' : 0.8,
				'traj_lws' : 2,
				'show'     : True
			}
		)

if __name__ == '__main__':
	test_lambert_uv_earth_to_venus( plot = True )