/*
AID | Astrodynamics Interactive Demo with HTML/CSS/JavaScript, Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Planetary data script
*/

const EARTH = {
	'mu'      : 3.9860043543609598E+05,
	'radius'  : 6378.0,
	'omega'   : 2 * Math.PI / ( 23 * 3600 + 56 * 60.0 + 4.0 ),
	'frame'   : 'IAU_EARTH',
	'img'     : 'https://raw.githubusercontent.com/alfonsogonzalez/pages-test/minimum-functionality/images/earth-surface-1024-512.jpeg',
	'color'   : 'blue',
	'defaults': {
		'rx0': 6878.0, 'ry0': 0, 'rz0': 0, 'vx0': 0,   'vy0': 7.62, 'vz0': 0,   'dt0': 60, 'sim-time0': 2,
		'rx1': 6878.0, 'ry1': 0, 'rz1': 0, 'vx1': 1.1, 'vy1': 1.5,  'vz1': 8.0, 'dt1': 60, 'sim-time1': 2,
		'sma0': 8500.0,  'ecc0': 0.2, 'inc0': 60.0, 'ta0': 0.0, 'aop0': 50.0, 'raan0': 40.0,   'dt-k0': 60,  'sim-time-k0': 2,
		'sma1': 42164.0, 'ecc1': 0.0, 'inc1': 0.0,  'ta1': 0.0, 'aop1': 0.0,  'raan1': -100.0, 'dt-k1': 180, 'sim-time-k1': 1
	}
};

const MOON = {
	'mu'      : 4.9028000661637961E+03,
	'radius'  : 1737.1,
	'omega'   : Math.PI / ( 27 * 12 * 3600 ),
	'frame'   : 'IAU_MOON',
	'img'     : 'https://raw.githubusercontent.com/alfonsogonzalez/pages-test/minimum-functionality/images/moon-surface-1024-512.jpeg',
	'color'   : 'gray',
	'defaults': {
		'rx0': 1837.1, 'ry0': 0, 'rz0': 0,      'vx0': 0,    'vy0': 1.8, 'vz0': 0,   'dt0': 100, 'sim-time0': 2,
		'rx1': 0,      'ry1': 0, 'rz1': 1900.0, 'vx1': 0.05, 'vy1': 1.9, 'vz1': 0.0, 'dt1': 100, 'sim-time1': 2,
		'sma0': 1787.1, 'ecc0': 0.01, 'inc0': 80.0, 'ta0': 0.0, 'aop0': 50.0, 'raan0': 40.0, 'dt-k0': 100, 'sim-time-k0': 2,
		'sma1': 3000.0, 'ecc1': 0.4,  'inc1': 88.0, 'ta1': 0.0, 'aop1': 50.0, 'raan1': 40.0, 'dt-k1': 100, 'sim-time-k1': 1
	}
};

const MARS = {
	'mu'      : 4.282837362069909E+04,
	'radius'  : 3389.5,
	'omega'   : Math.PI / ( 12.3 * 3600 ),
	'frame'   : 'IAU_MARS',
	'img'     : 'https://raw.githubusercontent.com/alfonsogonzalez/pages-test/minimum-functionality/images/mars-surface-1024-512.jpeg',
	'color'   : 'red',
	'defaults': {
		'rx0': 3889.5, 'ry0': 0,      'rz0': 0,       'vx0': 0,   'vy0': 3.45, 'vz0': 0,     'dt0': 60, 'sim-time0': 4,
		'rx1': 179.0,  'ry1': 3186.0, 'rz1': -1765.0, 'vx1': 0.3, 'vy1': -1.7, 'vz1': -2.98, 'dt1': 60, 'sim-time1': 4,
		'sma0': 12000.0, 'ecc0': 0.7, 'inc0': 60.0, 'ta0': 0.0, 'aop0': 0.0,  'raan0': 0.0,  'dt-k0': 60, 'sim-time-k0': 2,
		'sma1': 4000.0,  'ecc1': 0.1, 'inc1': 30.0, 'ta1': 0.0, 'aop1': 50.0, 'raan1': 40.0, 'dt-k1': 60, 'sim-time-k1': 4
	}
};
