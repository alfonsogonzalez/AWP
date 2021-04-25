'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Hello world of Spacecraft class
Two-body propagation with J2 perturbation for 100 periods
'''

# Python standard libraries
# AWP libraries
from Spacecraft import Spacecraft as SC
from planetary_data import earth

if __name__ == '__main__':
	coes = [ earth[ 'radius' ] + 1000, 0.05, 30.0, 0.0, 0.0, 0.0 ]
	sc   = SC(
			{
			'coes'       : coes,
			'tspan'      : '1',
			'dt'         : 100.0,
			'orbit_perts': { 'J2': True }
			} )
	sc.plot_3d()