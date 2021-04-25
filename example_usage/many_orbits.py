'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Many orbits script
'''

# Python standard libraries
from sys import path
path.append( '../src/python_tools' )

# AWP libraries
from Spacecraft import Spacecraft as SC
from planetary_data import earth
import plotting_tools as pt

# 3rd party libraries
import numpy as np

aops   = np.arange( 0, 360, 90 )
incs   = np.arange( 0, 90,  20 )
tas    = [ 0, 180 ]
coes   = [ earth[ 'radius' ] + 10000, 0.05, 0.0, 0.0, 0.0, 0.0 ]
scs    = []
config = {
	'tspan': '1',
	'dt'   : 100.0
}

print( len( aops ) * len( incs ) * len( tas ) )

if __name__ == '__main__':
	for inc in incs:
		for aop in aops:
			for ta in tas:
				coes[ 2 ] = inc
				coes[ 4 ] = ta
				coes[ 5 ] = aop
				config[ 'coes' ] = coes
				sc = SC( config )
				scs.append( sc )

	rs = [ sc.states[ :, :3 ] for sc in scs ]
	pt.plot_orbits( rs,
		{
		'traj_lws': 1,
		'show'    : True
		} )