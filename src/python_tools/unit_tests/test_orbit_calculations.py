'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Orbit Calculations Library Unit Tests
'''

# 3rd party libraries
import pytest
import numpy as np

# AWP library
import orbit_calculations as oc

# Treat all warnings as errors
pytestmark = pytest.mark.filterwarnings( 'error' )

def test_two_body_ode_zero_division_expect_throw():
	with pytest.raises( RuntimeWarning ):
		oc.two_body_ode( 0.0, np.zeros( 6 ) )
