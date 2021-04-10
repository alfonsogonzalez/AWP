'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP

Hello world of Spacecraft class
Two-body propagation with J2 perturbation for 100 periods
'''

from sys import path
path.append( '../python_tools' )

from Spacecraft import Spacecraft as SC
from planetary_data import earth

if __name__ == '__main__':
	coes = [ earth[ 'radius' ] + 500, 0.05, 30.0, 0.0, 0.0, 0.0 ]
	sc   = SC(
			{
			'coes'       : coes,
			'tspan'      : '100',
			'dt'         : 100.0,
			'orbit_perts': { 'J2': True }
			} )
	sc.plot_3d( { 'show' : True } )


