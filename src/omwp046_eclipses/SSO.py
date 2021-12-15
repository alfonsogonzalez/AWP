'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Sun-synchronous orbit spacecraft eclipse calculations
'''

# AWP library
from Spacecraft import Spacecraft as SC
import spice_data as sd

# 3rd party libraries
import spiceypy as spice

if __name__ == '__main__':
	spice.furnsh( sd.leapseconds_kernel )
	spice.furnsh( sd.de432 )	

	sc = SC( {
		'date0': '2021-01-01',
		'coes' : [ 6378 + 890.0, 0.0, 99.0, 0, 0, 80 ],
		'tspan': '4',
		} )
	sc.calc_eclipses( vv = True )

	sc.plot_eclipse_array( {
		'time_unit': 'days',
		'show'     : True
	} )
