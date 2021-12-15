'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Orbit Calculations Library Unit Tests
'''

# 3rd party libraries
import pytest
import numpy    as np
import spiceypy as spice

# AWP library
import orbit_calculations as oc
import numerical_tools    as nt
import spice_data         as sd
import planetary_data     as pd

# Treat all warnings as errors
pytestmark = pytest.mark.filterwarnings( 'error' )

def test_two_body_ode_zero_division_expect_throw():
	with pytest.raises( RuntimeWarning ):
		oc.two_body_ode( 0.0, np.zeros( 6 ) )

def test_two_body_ode_ones():
	a = oc.two_body_ode( 0.0,
		np.array( [ 1.0, 0, 0, 0, 0, 0 ] ), mu = 1.0 )
	assert np.all( a == np.array( [ 0, 0, 0, -1.0, 0, 0 ] ) )

def test_umbra_basic_usage():
	spice.furnsh( sd.leapseconds_kernel )
	spice.furnsh( sd.de432 )

	earth   = { 'SPICE_ID': 399, 'diameter': 2 * 6378.0 }
	et      = spice.str2et( '2021-11-16' )
	r_earth = spice.spkpos( '399', et, 'J2000', 'LT', 'SUN' )[ 0 ]

	'''
	Spacecraft is set to be on the sunlit side of Earth
	'''
	r_sc = -nt.normed( r_earth ) * 6500.0
	assert oc.check_eclipse( et, r_sc, earth ) == -1

	'''
	Spacecraft is set to be in umbra
	'''
	r_sc = nt.normed( r_earth ) * 6500.0
	assert oc.check_eclipse( et, r_sc, earth ) == 2

def test_penumbra_edge_cases():
	spice.furnsh( sd.leapseconds_kernel )
	spice.furnsh( sd.de432 )

	Dp       = 2 * 6378.0
	alt      = 600.0
	proj_mag = 6378.0 + alt
	et       = spice.str2et( '2021-11-16' )
	r_earth  = spice.spkpos( '399', et, 'J2000', 'LT', 'SUN' )[ 0 ]
	s_hat    = nt.normed( r_earth )
	v_perp   = nt.normed( np.cross( s_hat, [ 1, 0, 0 ] ) )
	Xp       = ( Dp * nt.norm( r_earth ) ) / ( pd.sun[ 'diameter' ] + Dp )
	alphap   = np.arcsin( Dp / ( 2 * Xp ) )
	kappa    = ( Xp + proj_mag ) * np.tan( alphap )

	r_sc0 = proj_mag * s_hat + v_perp * kappa * 1.01
	r_sc1 = proj_mag * s_hat + v_perp * kappa * 0.99

	assert oc.check_eclipse( et, r_sc0, pd.earth ) == -1
	assert oc.check_eclipse( et, r_sc1, pd.earth ) ==  1

def test_find_eclipses_basic_usage():
	spice.furnsh( sd.leapseconds_kernel )

	a = np.array( [
		-1, -1, -1, -1, 1, 2, 2, 2, 1, 1, -1, -1, 2, 2, 2, -1, -1,
		-1, 2, 2, 2, 1, -1, -1, -1, 1, 1, -1, -1 ] )
	ets = range( len( a ) )

	eclipses = oc.find_eclipses( ets, a, vv = True )

	assert len( eclipses[ 'idxs' ] ) == 4
	assert eclipses[ 'idxs' ][ 0 ] == ( 3, 9 )
	assert eclipses[ 'idxs' ][ 1 ] == ( 11, 14 )
	assert eclipses[ 'idxs' ][ 2 ] == ( 17, 21 )
	assert eclipses[ 'idxs' ][ 3 ] == ( 24, 26 )
