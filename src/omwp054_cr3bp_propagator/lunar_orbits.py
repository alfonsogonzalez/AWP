'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Create CR3BP 3D near-lunar orbits plot
'''

# AWP library
import CR3BP
import plotting_tools as pt

EM = CR3BP.CR3BP_SYSTEMS[ 'earth-moon' ]

if __name__ == '__main__':
	state1      = [ 1 - EM[ 'mu' ], 0, 0.005, 2.1, 0, 0 ]
	state2      = [ 1 - EM[ 'mu' ], 0, 0.01, 1.5, 0, 0 ]
	cr3bp       = CR3BP.CR3BP( 'earth-moon' )
	tspans      = [ 3, 8 ]
	statei      = [ state1, state2 ]
	states_list = []

	for n in range( len( statei ) ):
		ets, states = cr3bp.propagate_orbit( statei[ n ], tspans[ n ] )
		states_list.append( states[ :, :3 ] )

	pt.plot_cr3bp_3d( EM[ 'mu' ], states_list, {
		'colors'     : [ 'lime', 'm' ],
		'azimuth'    : -178,
		'elevation'  : 1,
		'axes_custom': 0.002,
		'hide_axes'  : True,
		'legend'     : False,
		'show'       : True
		} )
