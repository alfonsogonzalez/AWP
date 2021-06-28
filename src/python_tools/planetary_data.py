'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Planetary Data Library
'''

# gravitational constant
G_meters = 6.67430e-11       # m**3 / kg / s**2
G        = G_meters * 10**-9 # km**3/ kg / s**2

earth = {
		'name'            : 'Earth',
		'spice_name'      : 'EARTH',
		'SPICE_ID'        : 399,
		'mass'            : 5.972e24,
		'mu'              : 5.972e24 * G,
		'radius'          : 6378.0,
		'J2'              : 1.081874e-3,
		'sma'             : 149.596e6, # km
		'SOI'             : 926006.6608, # km
		'deorbit_altitude': 100.0, # km
		'cmap'            : 'Blues',
		'body_fixed_frame': 'ITRF93'
		}

jupiter = {
		'name'            : 'Jupiter',
		'spice_name'      : 'JUPITER BARYCENTER',
		'SPICE_ID'        : 5,
		'mass'            : 1.898e27,
		'mu'              : 1.26686e8,
		'radius'          : 71490.0,
		'sma'             : 778.570e6, # km
		'deorbit_altitude': 1000.0,    # km
		'SOI'             : 48.2e6     # km
}

saturn = {
	'name'            : 'Saturn',
	'spice_name'      : 'SATURN BARYCENTER',
	'SPICE_ID'        : 6,
	'mass'            : 568.34e24,
	'radius'          : 58232.0,
	'mu'              : 37.931e6,
	'sma'             : 1433.529e6,
	'deorbit_altitude': 1000.0,
	'SOI'             : 54890347.727
}

sun = {
	'name'            : 'Sun',
	'SPICE_ID'        : 10,
	'mass'            : 1.989e30,
	'mu'              : 1.989e30 * G,
	'radius'          : 695510.0,
	'deorbit_altitude': 1.2 * 695510.0,
	'cmap'            :'gist_heat'
}
