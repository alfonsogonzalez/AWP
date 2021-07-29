'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Interplanetary Trajectory V-Infinity Matcher (ITVIM) Unit Tests
'''

# 3rd party libraries
import pytest
import numpy    as np
import spiceypy as spice

# AWP library
from ITVIM import ITVIM
import numerical_tools as nt
import planetary_data  as pd
import spice_data      as sd

# Treat all warnings as errors
pytestmark = pytest.mark.filterwarnings( 'error' )

def test_ITVIM_empty_sequence_expect_throw():
	with pytest.raises( RuntimeError ):
		ITVIM( {} )

def test_ITVIM_EME_1963_2_year( plot = False ):
	'''
	Earth-Mars-Earth (EME) 2 year trajectory
	launching in 1963
	Example comes from Richard Battin's book
	called "Astronautical Guidance"
	'''
	spice.furnsh( sd.leapseconds_kernel )
	spice.furnsh( sd.de432 )

	sequence = [ 
		{
		'planet': 3,
		'time'  : '1963-06-21',
		'tm'    : -1
		},
		{
		'planet'   : 4,
		'planet_mu': pd.mars[ 'mu' ],
		'time'     : '1964-12-30 20:20:21.5',
		'tm'       : 1,
		'tol'      : 1e-5
		},
		{
		'planet': 3,
		'time'  : '1965-05-14',
		'tol'   : 1e-5
		}
	]
	itvim = ITVIM( { 'sequence': sequence } )
	itvim.print_summary()

	vinf_target0 = 18200.0 * nt.fps2kms
	vinf_target1 = 28852.0 * nt.fps2kms
	vinf_tol     = 0.05
	rp_target    = 7892.0 * nt.mi2km + pd.mars[ 'radius' ]
	rp_tol       = 1
	t0_target    = spice.str2et( '1963-06-21' )
	t1_target    = spice.str2et( '1964-12-31' )
	t2_target    = spice.str2et( '1963-06-21' )
	t_tol        = 1 * 24 * 3600.0

	assert itvim.seq[ 0 ][ 'v_infinity' ] == pytest.approx(
		vinf_target0, abs = vinf_tol )
	assert itvim.seq[ 1 ][ 'v_infinity' ] == pytest.approx(
		vinf_target1, abs = vinf_tol )
	assert itvim.seq[ 1 ][ 'periapsis' ] == pytest.approx(
		rp_target, abs = rp_tol )
	assert itvim.seq[ 1 ][ 'et' ] == pytest.approx(
		t1_target, abs = t_tol )
	
	if plot:
		itvim.plot_orbits()

def test_EVME_1966( plot = False ):
	'''
	Earth-Venus-Mars-Earth (EVME) 2 year trajectory
	launching in 1966
	Example comes from Richard Battin's book
	called "Astronautical Guidance"
	'''
	spice.furnsh( sd.leapseconds_kernel )
	spice.furnsh( sd.de432 )

	sequence = [ 
		{
		'planet': 3,
		'time'  : '1966-02-10',
		'tm'    : -1
		},
		{
		'planet'   : 2,
		'planet_mu': pd.venus[ 'mu' ],
		'time'     : '1966-07-07',
		'tm'       : 1,
		'tol'      : 1e-5
		},
		{
		'planet'   : 4,
		'planet_mu': pd.mars[ 'mu' ],
		'time'     : '1967-01-10',
		'tm'       : -1,
		'tol'      : 1e-5
		},
		{
		'planet'   : 3,
		'planet_mu': pd.earth[ 'mu' ],
		'time'     : '1967-12-18',
		'tol'      : 1e-5
		}
	]
	itvim = ITVIM( { 'sequence': sequence } )
	itvim.print_summary()

	t0_target = spice.str2et( '1966-02-06' )
	t1_target = spice.str2et( '1966-07-09' )
	t2_target = spice.str2et( '1967-01-24' )
	t3_target = spice.str2et( '1967-12-17' )
	t_targets = [ t0_target, t1_target, t2_target, t3_target ]
	t_tol     = 90 * 24 * 3600.0 # t2_target is about 3 days different

	if plot:
		itvim.plot_orbits( {
			'planets'  : [ pd.venus, pd.earth, pd.mars ],
			'colors'   : [ 'm', 'c', 'lime' ],
			'sc_labels': [ 'SC0', 'SC1', 'SC2' ],
			'traj_lws' : 2,
			'show'     : True
			} )

if __name__ == '__main__':
	test_ITVIM_EME_1963_2_year( plot = True )
	test_EVME_1966( plot = True )