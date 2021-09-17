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

def write_bsp( ets, states, args = {} ):
	'''
	Write or append to a BSP / SPK kernel from a NumPy array
	'''
	_args = {
		'bsp_fn'   : 'traj.bsp',
		'spice_id' : -999,
		'center'   : 399,
		'frame'    : 'J2000',
		'degree'   : 5,
		'verbose'  : True,
		'new'      : True,
		'comments' : '',
	}
	for key in args.keys():
		_args[ key ] = args[ key ]

	if _args[ 'new' ]:
		handle = spice.spkopn( _args[ 'bsp_fn' ],
			'SPK_file', len( _args[ 'comments' ] ) )
		action = 'Wrote'
	else:
		handle = spice.spkopa( _args[ 'bsp_fn' ] )
		action = 'Updated'

	spice.spkw09( handle, _args[ 'spice_id' ], _args[ 'center' ],
		_args[ 'frame'  ], ets[ 0 ], ets[ -1 ], '0',
		_args[ 'degree' ], len( ets ),
		states.tolist(), ets.tolist() )

	spice.spkcls( handle )

	if _args[ 'verbose' ]:
		print( f'{action} { _args[ "bsp_fn" ] }.' )
