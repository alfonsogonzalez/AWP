'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Spacecraft Class Unit Tests
'''

# 3rd party libraries
import pytest
import numpy    as np
import spiceypy as spice

# AWP library
from Spacecraft import Spacecraft as SC
import planetary_data             as pd
import spice_data                 as sd

# Treat all warnings as errors
pytestmark = pytest.mark.filterwarnings( 'error' )

def test_Spacecraft_basic_propagation( plot = False ):
	sc = SC( {
		'coes' : [ pd.earth[ 'radius' ] + 1000.0, 0.0, 0.0, 0.0, 0.0, 0.0 ],
		'tspan': '1',
		'dt'   : 100.0,
		'rtol' : 1e-8
		} )
	assert sc.cb == pd.earth

	'''
	Since inclination is 0, all z-axis components of Spacecraft
	position and velocity should be 0
	'''
	assert np.all( sc.states[ :, 2 ] == 0.0 )
	assert np.all( sc.states[ :, 5 ] == 0.0 )

	'''
	Since there are no orbital perturbations, all COEs except
	true anomaly should	be close to constant
	(not exactly constant due to numerical error).
	However, since this is a circular orbit, periapsis is loosely
	defined, causing errors in true anomaly (not exactly linear),
	argument of periapsis (bounces back and forth between
	0 and 359.9 degrees), eccentricity (random noise), and
	semi-major axis (drift / random noise)
	'''
	sc.calc_coes()
	assert sc.coes_calculated
	assert pytest.approx(
		sc.coes[ :, 0 ],
		abs = 1e-3 ) == pd.earth[ 'radius' ] + 1000.0          # sma
	assert pytest.approx( sc.coes[ :, 1 ], abs = 1e-6 ) == 0.0 # ecc
	assert np.all( sc.coes[ :, 2 ] == 0.0 )                    # inc
	assert np.all( sc.coes[ :, 5 ] == 0.0 )                    # raan

	sc.calc_apoapses_periapses()
	apse_diffs = sc.apoapses - sc.periapses
	assert pytest.approx( apse_diffs, abs = 1e-3 ) == 0.0

	if plot:
		sc.plot_coes()

def test_Spacecraft_inclination_latitude( plot = False ):
	spice.furnsh( sd.pck00010 )

	sc = SC( {
		'coes' : [ pd.earth[ 'radius' ] + 1000.0, 0.01, 50.0, 0.0, 0.0, 0.0 ],
		'tspan': '3',
		'dt'   : 10.0,
		'rtol' : 1e-8
		} )
	assert sc.cb == pd.earth

	'''
	Given that this spacecraft has 50 degrees inclination,
	the latitude coordinates should remain in between
	-50 and 50 degrees, since inclination is defined as
	the angle between the orbital plane and Earth's
	equatorial plane
	'''
	sc.calc_latlons()
	assert np.all( sc.latlons[ :, 2 ] <=  50.0 ) and\
		   np.all( sc.latlons[ :, 2 ] >= -50.0 )

	if plot:
		sc.plot_groundtracks()

if __name__ == '__main__':
	test_Spacecraft_basic_propagation( plot = True )
	test_Spacecraft_inclination_latitude( plot = True )
