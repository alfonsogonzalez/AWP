'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Geostationary orbit spacecraft eclipse calculations
'''

from Spacecraft import Spacecraft as SC
import spice_data as sd

import spiceypy as spice

if __name__ == '__main__':
	spice.furnsh( sd.leapseconds_kernel )
	spice.furnsh( sd.de432 )	

	sc = SC( {
		'date0': '2021-01-01',
		'coes' : [ 42164, 0, 0, 0, 0, 0 ],
		'tspan': '365',
		} )
	sc.plot_3d()
	sc.calc_eclipses( vv = True )
	sc.plot_eclipse_array( {
		'time_unit': 'days',
		'show'     : True,
	} )
