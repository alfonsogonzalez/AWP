'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

3Blue1Brown's Summer of Math Exposition video entry
and Orbital Mechanics with Python 44
Gravity Assist Design via V-Infinity Matching to Explore
Our Solar System

Earth-Venus-Mars-Earth gravity assist interplanetary
trajectory implementation solved by the
Interplanetary Trajectory V-Infinity Matcher (ITVIM)
The function here is called by other scripts in this
directory
'''

# 3rd party libraries
import spiceypy as spice

# AWP library
from ITVIM import ITVIM
import planetary_data     as pd
import spice_data         as sd

def calc_EVME_1963():
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

	return itvim

if __name__ == '__main__':
	calc_EVME_1963()
