'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Numerical Tools Library Unit Tests
'''

# 3rd party libraries
import pytest
import numpy as np

# AWP library
import numerical_tools as nt

# Treat all warnings as errors
pytestmark = pytest.mark.filterwarnings( 'error' )

def test_norm_zero_vector():
	assert nt.norm( [ 0, 0, 0 ] ) == 0.0

def test_norm_basic_usage():
	assert nt.norm( [ 1.0, 0, 0 ] ) == 1.0

def test_norm_pythagorean():
	assert nt.norm( [ 3.0, 4.0 ] ) == 5.0

def test_normed_zero_division_expect_throw():
	with pytest.raises( RuntimeWarning ):
		nt.normed( np.zeros( 3 ) )

def test_frame_transform_same_frame():
	arr = np.array( [ [ 1.0, 0.0, 0.0 ], [ 1.0, 0.0, 0.0 ] ] )
	arr_transformed = nt.frame_transform(
		arr, 'J2000', 'J2000', [ 0.0, 0.0 ] )
	assert np.all( arr == arr_transformed )

def test_fdiff_cs_basic_usage():
	f  = lambda x, _: x ** 2.0
	x0 = 3.5
	dx = 1e-5
	assert pytest.approx( 7.0, dx ) == nt.fdiff_cs( f, x0, dx )

def test_newton_root_single_basic_usage():
	f    = lambda x, _: 2.0 * x ** 2 - 2
	fp   = lambda x, _: 4.0 * x
	tol  = 1e-15
	args = { 'tol': tol }

	x0, _ = nt.newton_root_single( f, fp, -3.0, args )
	x1, _ = nt.newton_root_single( f, fp,  2.0, args )

	assert x0 == pytest.approx( -1.0, abs = tol )
	assert x1 == pytest.approx(  1.0, abs = tol )

def test_newton_root_single_fd_basic_usage():
	f    = lambda x, _: 2 * x ** 2 - 2
	tol  = 1e-15
	args = { 'tol': tol, 'diff_step': tol }

	x0, _ = nt.newton_root_single_fd( f, -3.0, args )
	x1, _ = nt.newton_root_single_fd( f,  2.0, args )

	assert x0 == pytest.approx( -1.0, tol )
	assert x1 == pytest.approx(  1.0, tol )

def test_vecs2angle_perpendicular():
	v0    = [ 1, 0, 0 ]
	v1    = [ 0, 1, 0 ]
	angle = nt.vecs2angle( v0, v1, deg = False )
	assert angle == np.pi / 2.0

def test_vecs2angle_45_deg():
	sqrt2 = np.sqrt( 2.0 )
	v0    = [ sqrt2, sqrt2,  0 ]
	v1    = [   0,     1,    0 ]
	angle = nt.vecs2angle( v0, v1, deg = False )
	assert angle == np.pi / 4.0

def test_frame_transform_invalid_dim_expect_throw():
	arr0 = np.zeros( ( 3, 7 ) )
	arr1 = np.zeros( ( 3, 2 ) )
	with pytest.raises( KeyError ):
		nt.frame_transform( arr0, 'J2000', 'IAU_EARTH', [] )
		nt.frame_transform( arr1, 'J2000', 'IAU_EARTH', [] )
