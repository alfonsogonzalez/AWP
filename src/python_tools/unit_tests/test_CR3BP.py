'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

CR3BP Class Unit Tests
'''

# 3rd party libraries
import pytest

# AWP library
from CR3BP import CR3BP

# Treat all warnings as errors
pytestmark = pytest.mark.filterwarnings( 'error' )

def test_CR3BP_invalid_system():
	with pytest.raises( RuntimeError ):
		CR3BP( 'invalid-name' )

def test_CR3BP_periodic_orbits( plot = False ):
	states0 = [
		[ 0.994,    0, 0, 0, -0.21138987966945026683e1, 0 ],
		[ 0.997,    0, 0, 0, -0.16251217072210773125e1, 0 ],
		[ 0.879962, 0, 0, 0, -0.38089067106386964470,   0 ],
		[ 0.1003e1, 0, 0, 0, -0.14465123738451062297e1, 0 ]
	]
	tspans = [ 0.54367954392601899690e1, 0.22929723423442969481e2,
			   0.19138746281183026809e2, 0.12267904265603897140e2 ]
	ns     = [ 1, 4, 7, 10 ]
	args   = { 'atol': 3e-14, 'rtol': 3e-14	}
	cr3bp  = CR3BP( 'earth-moon' )

	for n in range( len( states0 ) ):
		ets, states = cr3bp.propagate_orbit( states0[ n ], tspans[ n ], args )
		assert pytest.approx( states[ -1 ] - states[ 0 ], abs = 1e-6 ) == 0
		assert ets[ -1 ] == tspans[ n ]

		if plot:
			cr3bp.plot_2d( { 'title': f'P{ns[n]}' } )

if __name__ == '__main__':
	test_CR3BP_periodic_orbits( plot = True )
