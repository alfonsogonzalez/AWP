'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

3Blue1Brown's Summer of Math Exposition video entry
and Orbital Mechanics with Python 44
Gravity Assist Design via V-Infinity Matching to Explore
Our Solar System

Illustration of how a pure rotation in velocity vector
changes angular momentum and eccentricity of an orbit
'''

# 3rd party libraries
import numpy as np

# AWP library
from Spacecraft import Spacecraft as SC
import orbit_calculations as oc
import numerical_tools    as nt
import plotting_tools     as pt
import planetary_data     as pd

if __name__ == '__main__':
	periapsis = pd.earth[ 'radius' ] + 4000.0 # km
	coes      = [ periapsis / 0.3, 0.7, 0, 30.0, 0, 0 ]
	state     = oc.coes2state( coes )
	v_rot     = np.dot( nt.Cz( 40.0 * nt.d2r ), state[ 3: ] )
	state_rot = np.concatenate( ( state[ :3 ], v_rot ) )

	sc0    = SC( { 'orbit_state': state,     'tspan': '1' } )
	sc_rot = SC( { 'orbit_state': state_rot, 'tspan': '1' } )

	pt.plot_orbits( [ sc0.states[ :, :3 ], sc_rot.states[ :, :3 ] ],
		{
		'labels'     : [ 'Before', 'After' ],
		'colors'     : [ 'c', 'm' ],
		'azimuth'    : -90.0,
		'elevation'  :  90.0,
		'axes_custom': 36000.0,
		'traj_lws'   : 2.5,
		'show'       : True
		} )
