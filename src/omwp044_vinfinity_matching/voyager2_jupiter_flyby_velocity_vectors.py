'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

3Blue1Brown's Summer of Math Exposition video entry
and Orbital Mechanics with Python 44
Gravity Assist Design via V-Infinity Matching to Explore
Our Solar System

Create plot of Voyager 2 and Jupiter velocity vectors
before, during, and after flyby event

*********** NOTE ************
If you'd like to run this script, you must
run it from this directory so that the paths to the
SPICE kernels are correct. Or you can change the paths
to fit your needs
'''

# 3rd party libraries
import spiceypy as spice

# AWP library
import plotting_tools as pt

if __name__ == '__main__':

	spice.furnsh( '../../data/spice/lsk/naif0012.tls' )
	spice.furnsh( '../../data/spice/spk/de432s.bsp'   )
	spice.furnsh( 'voyager2_jupiter_flyby.bsp'   )
	
	et  = spice.str2et( '1979-07-09 TDB' )
	dt  = 10 * 24 * 3600.0
	et0 = et - dt
	et1 = et + dt

	v_arrive = spice.spkgeo( -32, et0, 'ECLIPJ2000', 0 )[ 0 ][ 3: ]
	v_depart = spice.spkgeo( -32, et1, 'ECLIPJ2000', 0 )[ 0 ][ 3: ]
	v_jup0   = spice.spkgeo( 5,   et0, 'ECLIPJ2000', 0 )[ 0 ][ 3: ]
	v_jup1   = spice.spkgeo( 5,   et1, 'ECLIPJ2000', 0 )[ 0 ][ 3: ]
	vinf0    = v_arrive - v_jup0
	vinf1    = v_depart - v_jup1
	vdelta   = v_depart - v_arrive

	v0 = { 'r': v_arrive, 'label': r'$\vec{v}_{arrive}$',   'color': 'm'  }
	v1 = { 'r': v_depart, 'label': r'$\vec{v}_{depart}$',   'color': 'm'  }
	v2 = { 'r': v_jup0,   'label': r'$\vec{v}_{Jupiter}$',  'color': 'C3' }
	v3 = { 'r': vinf0,    'label': r'$\vec{v}_{incoming}$', 'color': 'm'  }
	v4 = { 'r': vinf1,    'label': r'$\vec{v}_{outgoing}$', 'color': 'm'  }
	v5 = { 'r': vdelta,   'label': r'$\vec{\Delta v}$',   'color': 'lime' }

	pt.plot_orbits( [], {
		'vector_texts'     : True,
		'vector_text_scale': 1,
		'cb_radius'        : 0.4,
		'dist_unit'        : r'$\dfrac{km}{s}$',
		'axes_custom'      : 25.0,
		'azimuth'          : -49,
		'elevation'        : 90,
		'hide_axes'        : True,
		'show'             : True
		},
		vectors = [ v0, v1, v2, v5] )

	pt.plot_orbits( [], {
		'vector_texts'     : True,
		'vector_text_scale': 1,
		'cb_radius'        : 0.1,
		'dist_unit'        : r'$\dfrac{km}{s}$',
		'axes_custom'      : 15.0,
		'azimuth'          : -44,
		'elevation'        : 87,
		'hide_axes'        : True,
		'show'             : True
		},
		vectors = [ v3, v4 ] )
