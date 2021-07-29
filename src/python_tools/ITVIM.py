'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Interplanetary Trajectory V Infinity Matcher (ITVIM)
Class Definition
'''

# AWP library
from Spacecraft import Spacecraft as SC
import orbit_calculations as oc
import planetary_data     as pd
import lamberts_tools     as lt
import numerical_tools    as nt
import spice_tools        as st
import plotting_tools     as pt
import spiceypy           as spice
import numpy              as np

def null_config():
	return {
		'sequence': [],
		'mu'      : pd.sun[ 'mu' ],
		'frame'   : 'ECLIPJ2000',
		'center'  : 0
	}

class ITVIM:
	'''
	Interplanetary Trajectory V-Infinity Matcher
	'''
	def __init__( self, config ):
		self.config = null_config()
		for key in config.keys():
			self.config[ key ] = config[ key ]
		self.seq = self.config[ 'sequence' ]

		if not self.seq:
			raise RuntimeError( 'ITVIM was passed in an empty sequence.' )

		for step in self.seq:
			if type( step[ 'time' ] ) == str:
				step[ 'et'       ] = spice.str2et( step[ 'time' ] )
				step[ 'time_cal' ] = step[ 'time' ]
			else:
				step[ 'et'       ] = step[ 'time' ]
				step[ 'time_cal' ] = spice.et2utc( step[ 'time' ], 'C', 5 )

		self.n_steps = len( self.seq )
		self.calc_traj()

	def calc_traj( self ):
		et0    = self.seq[ 0 ][ 'et' ]
		et1    = self.seq[ 1 ][ 'et' ]
		tof    = et1 - et0
		state0 = spice.spkgeo( self.seq[ 0 ][ 'planet' ], et0,
			self.config[ 'frame' ], self.config[ 'center' ] )[ 0 ]
		state1 = spice.spkgeo( self.seq[ 1 ][ 'planet' ], et1,
			self.config[ 'frame' ], self.config[ 'center' ] )[ 0 ]

		v0_sc, v1_sc = lt.lamberts_universal_variables(
			state0[ :3 ], state1[ :3 ], tof,
			{ 'mu': self.config[ 'mu' ], 'tm': self.seq[ 0 ][ 'tm' ] } )

		self.seq[ 0 ][ 'tof'             ] = tof
		self.seq[ 0 ][ 'state_sc_depart' ] = np.concatenate(
			( state0[ :3 ], v0_sc ) )
		self.seq[ 0 ][ 'periapsis'       ] = 0.0
		self.seq[ 0 ][ 'turn_angle'      ] = 0.0
		self.seq[ 0 ][ 'v_infinity'      ] = nt.norm( v0_sc - state0[ 3: ] )

		self.seq[ 1 ][ 'state_sc_arrive' ] = np.concatenate( 
			( state1[ :3 ], v1_sc ) )
		self.seq[ 1 ][ 'v_infinity'      ] = nt.norm( v1_sc - state1[ 3: ] )

		for n in range( 1, self.n_steps - 1 ):
			seq0      = self.seq[ n     ]
			seq1      = self.seq[ n + 1 ]
			et0       = seq0[ 'et' ]
			et1       = seq1[ 'et' ]
			tof_guess = et1 - et0

			tof, v_sc_depart, v_sc_arrive = oc.vinfinity_match(
				seq0[ 'planet' ], seq1[ 'planet' ],
				seq0[ 'state_sc_arrive' ][ 3: ],
				et0, tof_guess, seq0 )

			state0 = spice.spkgeo( seq0[ 'planet' ], et0,
				self.config[ 'frame' ], self.config[ 'center' ] )[ 0 ]
			state1 = spice.spkgeo( seq1[ 'planet' ], et0 + tof,
				self.config[ 'frame' ], self.config[ 'center' ] )[ 0 ]

			vinf_i = seq0[ 'state_sc_arrive' ][ 3: ] - state0[ 3: ]
			vinf_o = v_sc_depart - state0[ 3: ]

			seq0[ 'tof'        ] = tof
			seq0[ 'tof_days'   ] = tof * nt.sec2day
			seq0[ 'turn_angle' ] = nt.vecs2angle( vinf_i, vinf_o ) / 2.0
			seq0[ 'periapsis'  ] = oc.calc_close_approach(
				seq0[ 'turn_angle' ] * nt.d2r,
				seq0[ 'v_infinity' ], seq0[ 'planet_mu' ] )
			seq0[ 'state_sc_depart' ]  = np.concatenate(
				( state0[ :3 ], v_sc_depart ) )

			seq1[ 'state_sc_arrive' ] = np.concatenate(
				( state1[ :3 ], v_sc_arrive ) )
			seq1[ 'et'              ] = et0 + tof
			seq1[ 'time_cal'        ] = spice.et2utc(
				seq1[ 'et' ], 'C', 5 )
			seq1[ 'v_infinity'      ] = nt.norm(
				v_sc_arrive - state1[ 3: ] )

		self.seq[ -1 ][ 'tof'        ] = 0
		self.seq[ -1 ][ 'turn_angle' ] = 0
		self.seq[ -1 ][ 'periapsis'  ] = 0

	def print_summary( self ):
		print( '************************************' )
		print( 'ITVIM Summary' )
		print( '************************************' )
		for n in range( self.n_steps ):
			tof_days = self.seq[ n ][ 'tof' ] * nt.sec2day
			print( f'Segment {n}:' )
			print( f'Time: {self.seq[n]["time_cal"]}')
			print( f'Time of Flight: {tof_days:.2f} days' )
			print( f'V Infinity: {self.seq[n]["v_infinity"]:.2f} km/s' )
			print( f'Turn Angle: {self.seq[n]["turn_angle"]:.2f} degrees' )
			print( f'Close Approach: {self.seq[n]["periapsis"]:.2f} km' )
			print()

	def plot_orbits( self, args = { 'show': True } ):
		_args = {
			'dt'       : 5000,
			'cb'       : pd.sun,
			'planets'  : [ pd.earth, pd.mars ],
			'colors'   : [ 'm', 'c' ],
			'sc_labels': [ 'SC 0', 'SC 1' ],
			'dist_unit': 'AU',
			'3d'       : True,
			'show'     : False,
			'filename' : None,
			'write_bsp': False
		}
		for key in args.keys():
			_args[ key ] = args[ key ]
		_args[ 'labels' ]  = _args[ 'sc_labels' ] +\
			[ p[ 'name' ] for p in _args[ 'planets' ] ]
		_args[ 'colors' ] += [
			planet[ 'traj_color' ] for planet in _args[ 'planets' ] ]

		rs        = []
		points    = []
		sc_config = {
			'dt'   : _args[ 'dt' ],
			'cb'   : _args[ 'cb' ],
			'frame': self.config[ 'frame' ]
		}

		for n in range( self.n_steps - 1 ):
			sc_config[ 'et0'         ] = self.seq[ n ][ 'et' ]
			sc_config[ 'tspan'       ] = self.seq[ n ][ 'tof' ]
			sc_config[ 'orbit_state' ] = self.seq[ n ][ 'state_sc_depart' ]
			sc                         = SC( sc_config )

			rs.append( sc.states[ :, :3 ] )
			points.append( {
				'x': sc.states[ -1, 0 ],
				'y': sc.states[ -1, 1 ],
				'z': sc.states[ -1, 2 ],
				'label': f'SC {n} end'
				} )
		_args[ 'points' ] = points
		
		ets = np.arange( self.seq[ 0 ][ 'et' ],
			self.seq[ -1 ][ 'et' ] + _args[ 'dt' ],
			_args[ 'dt' ] )

		for planet in _args[ 'planets' ]:
			rs.append(
				st.calc_ephemeris( planet[ 'SPICE_ID' ], ets,
					self.config[ 'frame' ],
					self.config[ 'center' ] )[ :, :3 ] )

		pt.plot_orbits( rs, _args )
