'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

SPICE convenience functions using SpiceyPy
'''

# 3rd party libraries
import spiceypy as spice
from numpy import array, zeros

def calc_ephemeris( target, ets, frame, observer ):
	'''
	Convenience wrapper for spkezr and spkgeo
	'''

	if type( target ) == str:
		return array( spice.spkezr( target, ets, frame, 'NONE', observer )[ 0 ] )

	else:
		n_states = len( ets )
		states   = zeros( ( n_states, 6 ) )
		for n in range( n_states ):
			states[ n ] = spice.spkgeo( target, ets[ n ], frame, observer )[ 0 ]
		return states