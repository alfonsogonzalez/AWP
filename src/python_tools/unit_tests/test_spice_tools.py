'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

SPICE Tools Library Unit Tests
'''

# Python standard libraries
import os

# 3rd party libraries
import pytest
import numpy    as np
import spiceypy as spice

# AWP library
import spice_tools     as st
import spice_data      as sd
import numerical_tools as nt
from Spacecraft import Spacecraft as SC

# Treat all warnings as errors
pytestmark = pytest.mark.filterwarnings( 'error' )

def test_read_write_bsp( plot = False ):
	'''
	Propagate a 30 degree inclination orbit (20 periods),
	write BSP kernel, then read back the BSP kernel, ensuring
	that latitudes are within +-30 degrees before and after
	writing kernel
	'''
	spice.furnsh( sd.pck00010 )

	sc = SC( {
		'coes' : [ 8000.0, 0.01, 30.0, 0, 0, 0 ],
		'tspan': '20'
		} )

	'''
	Ensure latitudes are +-30 degrees
	'''
	sc.calc_latlons()
	assert np.all( sc.latlons[ :, 2 ] <=  30.0 )
	assert np.all( sc.latlons[ :, 2 ] >= -30.0 )

	'''
	spice.spkopn will error if a bsp with the requested
	filename already exists
	'''
	filename = 'test_read_write_bsp.bsp'
	if os.path.isfile( filename ):
		os.remove( filename )

	'''
	Write bsp with all the default arguments except filename
	'''
	st.write_bsp( sc.ets, sc.states[ :, :6 ],
		{ 'bsp_fn': filename } )

	'''
	Now read back the bsp and ensure that
	latitudes are still within +-30 degrees
	'''
	spice.furnsh( filename )
	states  = st.calc_ephemeris( -999, sc.ets, 'IAU_EARTH', 399 )
	latlons = nt.cart2lat( states[ :, :3 ] )

	assert np.all( latlons[ :, 2 ] <=  30.0 )
	assert np.all( latlons[ :, 2 ] >= -30.0 )

	os.remove( filename )
