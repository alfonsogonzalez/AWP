'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

CR3BP lagrange point orbits with initial conditions
slightly perturbed in x-position
'''

# AWP library
import CR3BP
import plotting_tools as pt

EM   = CR3BP.CR3BP_SYSTEMS[ 'earth-moon' ]
Ly   = 3 ** 0.5 / 2.0
xl45 = 0.5 - EM[ 'mu' ]
dx   = -0.01

if __name__ == '__main__':
	state1      = [ EM[ 'L1' ], 0, 0, 0, 0, 0 ]
	state2      = [ EM[ 'L2' ], 0, 0, 0, 0, 0 ]
	state3      = [ EM[ 'L3' ], 0, 0, 0, 0, 0 ]
	state4      = [ xl45,  Ly, 0, 0, 0, 0 ]
	state5      = [ xl45, -Ly, 0, 0, 0, 0 ]
	cr3bp       = CR3BP.CR3BP( 'earth-moon' )
	tspan       = 40.0
	statei      = [ state1, state2, state3, state4, state5 ]
	states_list = []

	for n in range( 5 ):
		statei[ n ][ 0 ] += dx
		ets, states = cr3bp.propagate_orbit( statei[ n ], tspan )
		states_list.append( states[ :, :3 ] )

	pt.plot_cr3bp_2d( EM[ 'mu' ], states_list, {
		'colors': [ 'r', 'g', 'b', 'm', 'w' ],
		'labels': [ 'L1', 'L2', 'L3', 'L4', 'L5' ],
		'show'  : True
		} )
