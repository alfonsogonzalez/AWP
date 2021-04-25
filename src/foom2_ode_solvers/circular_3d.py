'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP

Fundamentals of Orbital Mechanics 2
Ordinary Differential Equations (ODEs) Solvers
https://www.youtube.com/watch?v=8-SyHZb7w40

Acceleration, Velocity and Position subplots script
for circular orbit
'''

from Spacecraft import Spacecraft as SC
import orbit_calculations as oc

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'dark_background' )

a    = 8078.0
coes = [ a, 0.0, 0.0, 0.0, 0.0, 0.0 ]

sc_config = {
	'coes' : coes,
	'tspan': '1.0',
	'dt'   : 100.0
}

fn = '/mnt/c/Users/alfon/AWP/foom2_ode_solvers/eq_3d.png'

if __name__ == '__main__':
	sc = SC( sc_config )
	sc.plot_3d( {
		'colors'   : [ 'c' ],
		'elevation': 90,
		'azimuth'  : 270,
		'hide_axes': True,
		'legend'   : False,
		'filename' : fn,
		'dpi'      : 300
		} )


