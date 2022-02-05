'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP

Plotting Tools Library
'''

from copy import copy
import os

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'dark_background' )

import cities_lat_long

time_handler = {
	'seconds': { 'coeff': 1.0,        'xlabel': 'Time (seconds)' },
	'hours'  : { 'coeff': 3600.0,     'xlabel': 'Time (hours)'   },
	'days'   : { 'coeff': 86400.0,    'xlabel': 'Time (days)'    },
	'years'  : { 'coeff': 31536000.0, 'xlabel': 'Time (years)'   }
}

dist_handler = {
	'km'    : 1.0,
	'ER'    : 1 / 6378.0,
	'JR'    : 1 / 71490.0,
	'AU'    : 6.68459e-9,
	r'$\dfrac{km}{s}$': 1.0
}

COLORS = [ 
	'm', 'deeppink', 'chartreuse', 'w', 'springgreen', 'peachpuff',
	'white', 'lightpink', 'royalblue', 'lime', 'aqua' ] * 100

COASTLINES_COORDINATES_FILE = os.path.join(
	os.path.dirname( os.path.realpath( __file__ ) ),
	os.path.join( '..', '..', 'data', 'earth_data', 'coastlines.csv' )
	)

EARTH_SURFACE_IMAGE = os.path.join(
	os.path.dirname( os.path.realpath( __file__ ) ),
	os.path.join( '..', '..', 'data', 'earth_data', 'earth_surface.png' )
	)

JUPITER_SURFACE_IMAGE = os.path.join(
	os.path.dirname( os.path.realpath( __file__ ) ),
	os.path.join( '..', '..', 'data', 'jupiter_data', 'jupiter_surface.png' )
	)

SURFACE_BODY_MAP = {
	'earth'  : EARTH_SURFACE_IMAGE,
	'jupiter': JUPITER_SURFACE_IMAGE
}

CITY_COLORS = [ 
	'w', 'deeppink', 'chartreuse', 'magenta', 'springgreen', 'peachpuff',
	'white', 'lightpink', 'royalblue', 'lime', 'aqua' ] * 100

def plot_reference_frames( frames, args, vectors = [], plots = [], planes = [] ):
	_args = {
		'figsize'       : ( 12, 12 ),
		'base_frame'    : True,
		'base_color'    : 'w',
		'base_label'    : 'Inertial',
		'frame_labels'  : [ '' ] * len( frames ),
		'frame_colors'  : [ 'm', 'c', 'b' ],
		'frame_zorders' : [ 10 ] * len( frames ),
		'vector_colors' : [ 'm', 'c', 'b' ],
		'vector_labels' : [ '' ] * len( vectors ),
		'vector_texts'  : True,
		'plots_labels'  : [ '' ] * len( plots ),
		'plots_colors'  : [ 'm' ],
		'plots_styles'  : [ '-' ] * len( plots ),
		'eq_plane'      : False,
		'eq_plane_color': 'c',
		'plane_labels'  : [ '' ] * len( planes ),
		'plane_colors'  : [ 'w' ],
		'plane_alphas'  : [ 0.3 ] * len( planes ),
		'no_axes'       : True,
		'axes_no_fill'  : False,
		'legend'        : True,
		'xlabel'        : 'X',
		'ylabel'        : 'Y',
		'zlabel'        : 'Z',
		'xlim'          : 1,
		'ylim'          : 1,
		'zlim'          : 1,
		'title'         : '',
		'azimuth'       : None,
		'elevation'     : None,
		'show'          : False,
		'filename'      : False,
		'dpi'           : 300,
		'frame_text_scale' : 1.1,
		'vector_text_scale': 1.3
	}
	for key in args.keys():
		_args[ key ] = args[ key ]

	fig      = plt.figure( figsize = _args[ 'figsize' ] )
	ax       = fig.add_subplot( 111, projection = '3d'  )
	zeros    = [ 0.0, 0.0, 0.0 ]
	n        = 0
	identity = [ [ 1, 0, 0 ], [ 0, 1, 0 ], [ 0, 0, 1 ] ]

	for frame in frames:
		'''
		The frame is passed into the quiver method by rows, but they
		are being plotted by columns. So the 3 basis vectors of the frame
		are the columns of the 3x3 matrix
		'''
		ax.quiver( zeros, zeros, zeros,
			frame[ 0, : ], frame[ 1, : ], frame[ 2, : ],
			color  = _args[ 'frame_colors'  ][ n ],
			label  = _args[ 'frame_labels'  ][ n ],
			zorder = _args[ 'frame_zorders' ][ n ] )

		if _args[ 'vector_texts' ]:
			frame *= _args[ 'frame_text_scale' ]
			ax.text( frame[ 0, 0 ], frame[ 1, 0 ], frame[ 2, 0 ], 'X',
				color = _args[ 'frame_colors' ][ n ] )
			ax.text( frame[ 0, 1 ], frame[ 1, 1 ], frame[ 2, 1 ], 'Y',
				color = _args[ 'frame_colors' ][ n ] )
			ax.text( frame[ 0, 2 ], frame[ 1, 2 ], frame[ 2, 2 ], 'Z',
				color = _args[ 'frame_colors' ][ n ] )
		n += 1

	if _args[ 'base_frame' ]:
		ax.quiver( zeros, zeros, zeros,
			identity[ 0 ], identity[ 1 ], identity[ 2 ],
			color  = _args[ 'base_color' ],
			label  = _args[ 'base_label' ],
			zorder = 0 )

		if _args[ 'vector_texts' ]:
			ax.text( _args[ 'frame_text_scale' ], 0, 0, 'X',
				color = _args[ 'base_color' ] )
			ax.text( 0, _args[ 'frame_text_scale' ], 0, 'Y',
				color = _args[ 'base_color' ] )
			ax.text( 0, 0, _args[ 'frame_text_scale' ], 'Z',
				color = _args[ 'base_color' ] )
	n = 0
	for plot in plots:
		ax.plot( plot[ :, 0 ], plot[ :, 1 ], plot[ :, 2 ],
			_args[ 'plots_colors' ][ n ] + _args[ 'plots_styles' ][ n ],
			label = _args[ 'plots_labels' ][ n ] )
		n += 1

	n = 0
	for vector in vectors:
		ax.quiver( 0, 0, 0,
			vector[ 0 ], vector[ 1 ], vector[ 2 ],
			color = _args[ 'vector_colors' ][ n ],
			label = _args[ 'vector_labels' ][ n ] )

		if _args[ 'vector_texts' ]:
			vector *= _args[ 'vector_text_scale' ]
			ax.text( vector[ 0 ], vector[ 1 ], vector[ 2 ],
				_args[ 'vector_labels' ][ n ],
				color = _args[ 'vector_colors' ][ n ] )
		n += 1

	n = 0
	for plane in planes:
		ax.plot_surface( plane[ 0 ], plane[ 1 ], plane[ 2 ],
			color  = _args[ 'plane_colors' ][ n ],
			alpha  = _args[ 'plane_alphas' ][ n ],
			zorder = 0 )

	ax.set_xlabel( _args[ 'xlabel' ] )
	ax.set_ylabel( _args[ 'ylabel' ] )
	ax.set_zlabel( _args[ 'zlabel' ] )
	ax.set_xlim( [ -_args[ 'xlim' ], _args[ 'xlim' ] ] )
	ax.set_ylim( [ -_args[ 'ylim' ], _args[ 'ylim' ] ] )
	ax.set_zlim( [ -_args[ 'zlim' ], _args[ 'zlim' ] ] )
	ax.set_box_aspect( [ 1, 1, 1 ] )
	ax.set_title( _args[ 'title' ] )

	if _args[ 'legend' ]:
		ax.legend()

	if _args[ 'no_axes' ]:
		ax.set_axis_off()

	if _args[ 'axes_no_fill' ]:
		ax.w_xaxis.pane.fill = False
		ax.w_yaxis.pane.fill = False
		ax.w_zaxis.pane.fill = False

	if _args[ 'azimuth' ] is not None:
		ax.view_init( elev = _args[ 'elevation' ],
					  azim = _args[ 'azimuth'   ] )

	if _args[ 'show' ]:
		plt.show()

	if _args[ 'filename' ]:
		plt.savefig( _args[ 'filename' ], dpi = _args[ 'dpi' ] )
		print( 'Saved', _args[ 'filename' ] )

	plt.close()

def plot_orbits( rs, args, vectors = [] ):
	_args = {
		'figsize'      : ( 10, 8 ),
		'labels'       : [ '' ] * len( rs ),
		'colors'       : COLORS[ : ],
		'traj_lws'     : 3,
		'dist_unit'    : 'km',
		'groundtracks' : False,
		'cb_radius'    : 6378.0,
		'cb_SOI'       : None,
		'cb_SOI_color' : 'c',
		'cb_SOI_alpha' : 0.7,
		'cb_axes'      : True,
		'cb_axes_mag'  : 2,
		'cb_cmap'      : 'Blues',
		'cb_axes_color': 'w',
		'axes_mag'     : 0.8,
		'axes_custom'  : None,
		'title'        : 'Trajectories',
		'legend'       : True,
		'axes_no_fill' : True,
		'hide_axes'    : False,
		'azimuth'      : False,
		'elevation'    : False,
		'show'         : False,
		'filename'     : False,
		'dpi'          : 300,
		'vector_colors': [ '' ] * len( vectors ),
		'vector_labels': [ '' ] * len( vectors ),
		'vector_texts' : False
	}
	for key in args.keys():
		_args[ key ] = args[ key ]

	fig = plt.figure( figsize = _args[ 'figsize' ] )
	ax  = fig.add_subplot( 111, projection = '3d'  )

	max_val = 0
	n       = 0

	for r in rs:
		_r = r.copy() * dist_handler[ _args[ 'dist_unit' ] ]

		ax.plot( _r[ :, 0 ], _r[ :, 1 ], _r[ : , 2 ],
			color = _args[ 'colors' ][ n ], label = _args[ 'labels' ][ n ],
			zorder = 10, linewidth = _args[ 'traj_lws' ] )
		ax.plot( [ _r[ 0, 0 ] ], [ _r[ 0 , 1 ] ], [ _r[ 0, 2 ] ], 'o',
			color = _args[ 'colors' ][ n ] )

		if _args[ 'groundtracks' ]:
			rg  = _r / np.linalg.norm( r, axis = 1 ).reshape( ( r.shape[ 0 ], 1 ) )
			rg *= _args[ 'cb_radius' ]

			ax.plot( rg[ :, 0 ], rg[ :, 1 ], rg[ :, 2 ], cs[ n ], zorder = 10 )
			ax.plot( [ rg[ 0, 0 ] ], [ rg[ 0, 1 ] ], [ rg[ 0, 2 ] ], cs[ n ] + 'o', zorder = 10 )			

		max_val = max( [ _r.max(), max_val ] )
		n += 1

	for vector in vectors:
		ax.quiver( 0, 0, 0,
			vector[ 'r' ][ 0 ], vector[ 'r' ][ 1 ], vector[ 'r' ][ 2 ],
			color = vector[ 'color' ], label = vector[ 'label' ] )

		if _args[ 'vector_texts' ]:
			vector[ 'r' ] *= _args[ 'vector_text_scale' ]
			ax.text( vector[ 'r' ][ 0 ], vector[ 'r' ][ 1 ], vector[ 'r' ][ 2 ],
				vector[ 'label' ],
				color = vector[ 'color' ] )

	_args[ 'cb_radius' ] *= dist_handler[ _args[ 'dist_unit' ] ]
	_u, _v = np.mgrid[ 0:2*np.pi:20j, 0:np.pi:20j ]
	_x     = _args[ 'cb_radius' ] * np.cos( _u ) * np.sin( _v )
	_y     = _args[ 'cb_radius' ] * np.sin( _u ) * np.sin( _v )
	_z     = _args[ 'cb_radius' ] * np.cos( _v )
	ax.plot_surface( _x, _y, _z, cmap = _args[ 'cb_cmap' ], zorder = 1 )

	if _args[ 'cb_SOI' ] is not None:
		_args[ 'cb_SOI' ] *= dist_handler[ _args[ 'dist_unit' ] ]
		_x *= _args[ 'cb_SOI' ] / _args[ 'cb_radius' ]
		_y *= _args[ 'cb_SOI' ] / _args[ 'cb_radius' ]
		_z *= _args[ 'cb_SOI' ] / _args[ 'cb_radius' ]
		ax.plot_wireframe( _x, _y, _z,
			color = _args[ 'cb_SOI_color' ],
			alpha = _args[ 'cb_SOI_alpha' ] )

	if _args[ 'cb_axes' ]:
		l       = _args[ 'cb_radius' ] * _args[ 'cb_axes_mag' ]
		x, y, z = [ [ 0, 0, 0 ], [ 0, 0, 0  ], [ 0, 0, 0 ] ]
		u, v, w = [ [ l, 0, 0 ], [ 0, l, 0 ], [ 0, 0, l ] ]
		ax.quiver( x, y, z, u, v, w, color = _args[ 'cb_axes_color' ] )

	xlabel = 'X (%s)' % _args[ 'dist_unit' ]
	ylabel = 'Y (%s)' % _args[ 'dist_unit' ]
	zlabel = 'Z (%s)' % _args[ 'dist_unit' ]

	if _args[ 'axes_custom' ] is not None:
		max_val = _args[ 'axes_custom' ]
	else:
		max_val *= _args[ 'axes_mag' ]

	ax.set_xlim( [ -max_val, max_val ] )
	ax.set_ylim( [ -max_val, max_val ] )
	ax.set_zlim( [ -max_val, max_val ] )
	ax.set_xlabel( xlabel )
	ax.set_ylabel( ylabel )
	ax.set_zlabel( zlabel )
	ax.set_box_aspect( [ 1, 1, 1 ] )
	ax.set_aspect( 'auto' )

	if _args[ 'azimuth' ] is not False:
		ax.view_init( elev = _args[ 'elevation' ],
					  azim = _args[ 'azimuth'   ] )
	
	if _args[ 'axes_no_fill' ]:
		ax.w_xaxis.pane.fill = False
		ax.w_yaxis.pane.fill = False
		ax.w_zaxis.pane.fill = False		

	if _args[ 'hide_axes' ]:
		ax.set_axis_off()

	if _args[ 'legend' ]:
		plt.legend()

	if _args[ 'filename' ]:
		plt.savefig( _args[ 'filename' ], dpi = _args[ 'dpi' ] )
		print( 'Saved', _args[ 'filename' ] )

	if _args[ 'show' ]:
		plt.show()

	plt.close()

def plot_states( ets, states, args ):
	_args = {
		'figsize'      : ( 16, 8 ),
		'colors'       : COLORS[ : ],
		'dist_unit'    : 'km',
		'time_unit'    : 'seconds',
		'lw'           : 2.5,
		'r_hlines'     : [],
		'v_hlines'     : [],
		'hline_lstyles': 'dashed',
		'title'        : 'Trajectories',
		'xlim'         : None,
		'r_ylim'       : None,
		'v_ylim'       : None,
		'legend'       : True,
		'show'         : False,
		'filename'     : False,
		'dpi'          : 300,
	}
	for key in args.keys():
		_args[ key ] = args[ key ]

	fig, ( ax0, ax1 ) = plt.subplots( 2, 1,
		figsize = _args[ 'figsize' ] )

	_args[ 'xlabel' ]     = time_handler[ _args[ 'time_unit' ] ][ 'xlabel' ]
	_args[ 'time_coeff' ] = time_handler[ _args[ 'time_unit' ] ][ 'coeff' ]
	ts     = ets[:] - ets[0]
	ts    /= _args[ 'time_coeff' ]
	rnorms = np.linalg.norm( states[ :, :3 ], axis = 1 )
	vnorms = np.linalg.norm( states[ :, 3: ], axis = 1 )

	if _args[ 'xlim' ] is None:
		_args[ 'xlim' ] = [ 0, ts[ -1 ] ]

	if _args[ 'r_ylim' ] is None:
		_args[ 'r_ylim' ] = [ states[ :, :3 ].min(), rnorms.max() ]

	if _args[ 'v_ylim' ] is None:
		_args[ 'v_ylim' ] = [ states[ :, 3: ].min(), vnorms.max() ]

	''' Positions '''
	ax0.plot( ts, states[ :, 0 ], 'r', label = r'$r_x$',
		linewidth = _args[ 'lw' ] )
	ax0.plot( ts, states[ :, 1 ], 'g', label = r'$r_y$',
		linewidth = _args[ 'lw' ] )
	ax0.plot( ts, states[ :, 2 ], 'b', label = r'$r_z$',
		linewidth = _args[ 'lw' ] )
	ax0.plot( ts, rnorms        , 'm', label = r'$Norms$',
		linewidth = _args[ 'lw' ] )

	ax0.grid( linestyle = 'dotted' )
	ax0.set_xlim( _args[ 'xlim'   ] )
	ax0.set_ylim( _args[ 'r_ylim' ] )
	ax0.set_ylabel( r'Position $(km)$')

	for hline in _args[ 'r_hlines' ]:
		ax0.hlines( hline[ 'val' ], ts[ 0 ], ts[ -1 ],
			color     = hline[ 'color' ],
			linestyle = _args[ 'hline_lstyles' ] )

	''' Velocities '''
	ax1.plot( ts, states[ :, 3 ], 'r', label = r'$r_x$',
		linewidth = _args[ 'lw' ] )
	ax1.plot( ts, states[ :, 4 ], 'g', label = r'$r_y$',
		linewidth = _args[ 'lw' ] )
	ax1.plot( ts, states[ :, 5 ], 'b', label = r'$r_z$',
		linewidth = _args[ 'lw' ] )
	ax1.plot( ts, vnorms        , 'm', label = r'$Norms$',
		linewidth = _args[ 'lw' ] )

	ax1.grid( linestyle = 'dotted' )
	ax1.set_xlim( _args[ 'xlim'   ] )
	ax1.set_ylim( _args[ 'v_ylim' ] )
	ax1.set_ylabel( r'Velocity $(\dfrac{km}{s})$' )
	ax1.set_xlabel( _args[ 'xlabel' ] )

	for hline in _args[ 'v_hlines' ]:
		ax1.hlines( hline[ 'val' ], ts[ 0 ], ts[ -1 ],
			color     = hline[ 'color' ],
			linestyle = _args[ 'hline_lstyles' ] )

	plt.suptitle( _args[ 'title' ] )
	plt.tight_layout()

	if _args[ 'legend' ]:
		ax0.legend()
		ax1.legend()

	if _args[ 'filename' ]:
		plt.savefig( _args[ 'filename' ], dpi = _args[ 'dpi' ] )
		print( 'Saved', _args[ 'filename' ] )

	if _args[ 'show' ]:
		plt.show()

	plt.close()

def plot_velocities( ets, vs, args ):
	_args = {
		'figsize'          : ( 16, 8 ),
		'dist_unit'        : 'km',
		'time_unit'        : 'seconds',
		'hlines'           : [],
		'hline_lstyles'    : 'dotted',
		'lw'               : 2,
		'labelsize'        : 15,
		'legend_fontsize'  : 20,
		'legend_framealpha': 0.3,
		'title'            : 'Trajectories',
		'xlim'             : None,
		'ylim'             : None,
		'legend'           : True,
		'show'             : False,
		'filename'         : False,
		'dpi'              : 300,
	}
	for key in args.keys():
		_args[ key ] = args[ key ]

	fig, ax0 = plt.subplots( 1, 1, figsize = _args[ 'figsize' ] )

	_args[ 'xlabel' ] = time_handler[ _args[ 'time_unit' ] ][ 'xlabel' ]
	time_coeff        = time_handler[ _args[ 'time_unit' ] ][ 'coeff'  ]

	_ets   = ets.copy() - ets[ 0 ]
	_ets  /= time_coeff
	vnorms = np.linalg.norm( vs, axis = 1 )

	if _args[ 'xlim' ] is None:
		_args[ 'xlim' ] = [ 0, _ets[ -1 ] ]

	if _args[ 'ylim' ] is None:
		_args[ 'ylim' ] = [ vs.min(), vnorms.max() ]

	ax0.plot( _ets, vs[ :, 0 ], 'r', label = r'$v_x$',
		linewidth = _args[ 'lw' ] )
	ax0.plot( _ets, vs[ :, 1 ], 'g', label = r'$v_y$',
		linewidth = _args[ 'lw' ] )
	ax0.plot( _ets, vs[ :, 2 ], 'b', label = r'$v_z$',
		linewidth = _args[ 'lw' ]  )
	ax0.plot( _ets, vnorms    , 'm', label = r'$Norms$',
		linewidth = _args[ 'lw' ] )

	ax0.grid( linestyle = 'dotted' )
	ax0.set_xlim( _args[ 'xlim'   ] )
	ax0.set_ylim( _args[ 'ylim' ] )
	ax0.set_xlabel( _args[ 'xlabel' ], size = _args[ 'labelsize' ] )
	ax0.set_ylabel( r'Velocity $(\dfrac{km}{s})$',
		size = _args[ 'labelsize' ] )

	for hline in _args[ 'hlines' ]:
		ax0.hlines( hline[ 'val' ], _ets[ 0 ], _ets[ -1 ],
			color     = hline[ 'color' ],
			linewidth = _args[ 'lw' ],
			linestyle = _args[ 'hline_lstyles' ] )

	plt.suptitle( _args[ 'title' ] )
	plt.tight_layout()

	if _args[ 'legend' ]:
		ax0.legend( fontsize = _args[ 'legend_fontsize' ],
			loc = 'upper right', framealpha = _args[ 'legend_framealpha' ] )

	if _args[ 'filename' ]:
		plt.savefig( _args[ 'filename' ], dpi = _args[ 'dpi' ] )
		print( 'Saved', _args[ 'filename' ] )

	if _args[ 'show' ]:
		plt.show()

	plt.close()

def plot_coes( ets, coes, args ):
	_args = {
		'figsize'  : ( 18, 9 ),
		'labels'   : [ '' ] * len( coes ),
		'lws'      : 1,
		'color'    : 'm',
		'grid'     : True,
		'title'    : 'COEs',
		'title_fs' : 25,
		'wspace'   : 0.3,
		'time_unit': 'seconds',
		'show'     : False,
		'filename' : False,
		'dpi'      : 300,
		'legend'   : True,
	}
	for key in args.keys():
		_args[ key ] = args[ key ]

	_args[ 'xlabel' ]     = time_handler[ _args[ 'time_unit' ] ][ 'xlabel' ]
	_args[ 'time_coeff' ] = time_handler[ _args[ 'time_unit' ] ][ 'coeff'  ]

	ts  = ets * _args[ 'time_coeff' ]
	ts -= ts[ 0 ]

	fig,( ( ax0, ax1, ax2 ),( ax3, ax4, ax5 ) ) = plt.subplots( 2, 3,
		figsize = _args[ 'figsize' ] )
	fig.suptitle( _args[ 'title' ], fontsize = _args[ 'title_fs' ] )

	# true anomaly
	n = 0
	for coe in coes:
		ax0.plot( ts, coe[ :, 3 ], _args[ 'color' ],
		label = _args[ 'labels' ][ n ] )
		n += 1
	ax0.set_ylabel( 'True Anomaly $(deg)$' )
	ax0.grid( linestyle = 'dotted' )

	# semi major axis
	n = 0
	for coe in coes:
		ax3.plot( ts, coe[ :, 0 ], _args[ 'color' ],
		label = _args[ 'labels' ][ n ] )
		n += 1
	ax3.set_ylabel( 'Semi-Major Axis $(km)$' )
	ax3.set_xlabel( _args[ 'xlabel' ] )
	ax3.grid( linestyle = 'dotted' )

	# eccentricity
	n = 0
	for coe in coes:
		ax1.plot( ts, coe[ :, 1 ], _args[ 'color' ],
		label = _args[ 'labels' ][ n ] )
		n += 1
	ax1.set_ylabel( 'Eccentricity' )
	ax1.grid( linestyle = 'dotted' )

	# inclination
	n = 0
	for coe in coes:
		ax4.plot( ts, coe[ :, 2 ], _args[ 'color' ],
		label = _args[ 'labels' ][ n ] )
		n += 1
	ax4.set_ylabel( 'Inclination $(deg)$' )
	ax4.set_xlabel( _args[ 'xlabel' ] )
	ax4.grid( linestyle = 'dotted' )

	# argument of periapsis
	n = 0
	for coe in coes:
		ax2.plot( ts, coe[ :, 4 ], _args[ 'color' ],
		label = _args[ 'labels' ][ n ] )
		n += 1
	ax2.set_ylabel( 'Argument of Periapsis $(deg)$' )
	ax2.grid( linestyle = 'dotted' )

	# right ascension of the ascending node
	n = 0
	for coe in coes:
		ax5.plot( ts, coe[ :, 5 ], _args[ 'color' ],
		label = _args[ 'labels' ][ n ] )
		n += 1
	ax5.set_xlabel( _args[ 'xlabel' ] )
	ax5.set_ylabel( 'RAAN $(deg)$' )
	ax5.grid( linestyle = 'dotted' )

	plt.subplots_adjust( wspace = _args[ 'wspace' ] )

	if _args[ 'show' ]:
		plt.show()

	if _args[ 'filename' ]:
		plt.savefig( _args[ 'filename' ], dpi = _args[ 'dpi' ] )

	plt.close()

def plot_groundtracks( coords, args ):
	_args = {
		'figsize'    : ( 18, 9 ),
		'markersize' : 1,
		'labels'     : [ '' ] * len( coords ),
		'city_names' : cities_lat_long.city_list0,
		'colors'     : [ 'c', 'r', 'b', 'g', 'w', 'y' ],
		'grid'       : True,
		'title'      : 'Groundtracks',
		'show'       : False,
		'filename'   : False,
		'dpi'        : 300,
		'city_colors': CITY_COLORS[ : ],
		'city_msize' : 3,
		'city_fsize' : 10,
		'legend'     : True,
		'surface_image': True,
		'surface_body' : 'earth',
		'plot_coastlines': False
	}
	for key in args.keys():
		_args[ key ] = args[ key ]

	plt.figure( figsize = _args[ 'figsize' ] )	

	if _args[ 'surface_image' ]:
		plt.imshow(
			plt.imread( SURFACE_BODY_MAP[ _args[ 'surface_body' ] ] ),
			extent = [ -180, 180, -90, 90 ] )

	if _args[ 'plot_coastlines' ]:
		coast_coords = np.genfromtxt( COASTLINES_COORDINATES_FILE,
			delimiter = ',' )

		plt.plot( coast_coords[ :, 0 ], coast_coords[ :, 1 ], 'mo',
			markersize = 0.3 )

	for n in range( len( coords ) ):
		plt.plot( [ coords[ n ][ 0, 1 ] ], [ coords[ n ][ 0, 2 ] ], 'o',
			color = _args[ 'colors' ][ n ], 
			label = _args[ 'labels' ][ n ] )
		plt.plot( coords[ n ][ 1:, 1 ], coords[ n ][ 1:, 2 ], 'o',
			color = _args[ 'colors' ][ n ],
			markersize = _args[ 'markersize' ] )

	# TODO save this as a .json
	cities = cities_lat_long.city_dict()
	n      = 0

	for city in _args[ 'city_names' ]:
		coords = cities[ city ]
		plt.plot( [ coords[ 1 ] ], [ coords[ 0 ] ], 'o',
			color      = _args[ 'city_colors' ][ n ],
			markersize = _args[ 'city_msize' ] )

		if n % 2 == 0:
			xytext = ( 0, 2 )
		else:
			xytext = ( 0, -8 )

		plt.annotate( city, [ coords[ 1 ], coords[ 0 ] ],
					  textcoords = 'offset points', xytext = xytext,
					  ha = 'center', color = _args[ 'city_colors' ][ n ],
					  fontsize = _args[ 'city_fsize' ]
					)
		n += 1

	plt.xlim( [ -180, 180 ] )
	plt.ylim( [ -90, 90 ] )
	plt.xticks( range( -180, 200, 20 ) )
	plt.yticks( range( -90, 100, 10 ) )
	plt.xlabel( r'Longitude (degrees $^\circ$)' )
	plt.ylabel( r'Latitude (degrees $^\circ$)' )
	plt.tight_layout()

	if _args[ 'legend' ]:
		plt.legend()

	if _args[ 'grid' ]:
		plt.grid( linestyle = 'dotted' )

	if _args[ 'show' ]:
		plt.show()

	if _args[ 'filename' ]:
		plt.savefig( _args[ 'filename' ], dpi = _args[ 'dpi' ] )

def plot_altitudes( ets, alts, args ):
	_args = {
		'figsize'          : ( 16, 8 ),
		'labels'           : [ '' ] * len( alts ),
		'dist_unit'        : 'km',
		'time_unit'        : 'seconds',
		'colors'           : [ 'm', 'lime', 'c' ],
		'hlines'           : [],
		'hline_lstyles'    : 'dotted',
		'lw'               : 2,
		'labelsize'        : 15,
		'legend_fontsize'  : 20,
		'legend_framealpha': 0.3,
		'title'            : 'Trajectories',
		'xlim'             : None,
		'ylim'             : None,
		'legend'           : True,
		'show'             : False,
		'filename'         : False,
		'dpi'              : 300,
	}
	for key in args.keys():
		_args[ key ] = args[ key ]

	fig, ax0 = plt.subplots( 1, 1, figsize = _args[ 'figsize' ] )

	_args[ 'xlabel' ] = time_handler[ _args[ 'time_unit' ] ][ 'xlabel' ]
	time_coeff        = time_handler[ _args[ 'time_unit' ] ][ 'coeff'  ]

	_ets    = ets - ets[ 0 ]
	_ets   /= time_coeff
	n       = 0
	min_val = 1e10
	max_val = 0

	for alt in alts:
		ax0.plot( _ets, alt, color = _args[ 'colors' ][ n ],
			label     = _args[ 'labels' ][ n ],
			linewidth = _args[ 'lw' ] )

		min_val = min( alt.min(), min_val )
		max_val = max( alt.max(), max_val )
		n      += 1

	if _args[ 'xlim' ] is None:
		_args[ 'xlim' ] = [ 0, _ets[ -1 ] ]

	if _args[ 'ylim' ] is None:
		_args[ 'ylim' ] = [ min_val * 0.9, max_val * 1.1 ]

	ax0.grid( linestyle = 'dotted' )
	ax0.set_xlim( _args[ 'xlim'   ] )
	ax0.set_ylim( _args[ 'ylim' ] )
	ax0.set_xlabel( _args[ 'xlabel' ], size = _args[ 'labelsize' ] )
	ax0.set_ylabel( r'Altitude $(km)$',
		size = _args[ 'labelsize' ] )

	for hline in _args[ 'hlines' ]:
		ax0.hlines( hline[ 'val' ], _ets[ 0 ], _ets[ -1 ],
			color     = hline[ 'color' ],
			linewidth = _args[ 'lw' ],
			linestyle = _args[ 'hline_lstyles' ] )

	plt.suptitle( _args[ 'title' ] )
	plt.tight_layout()

	if _args[ 'legend' ]:
		ax0.legend( fontsize = _args[ 'legend_fontsize' ],
			loc = 'upper right', framealpha = _args[ 'legend_framealpha' ] )

	if _args[ 'filename' ]:
		plt.savefig( _args[ 'filename' ], dpi = _args[ 'dpi' ] )
		print( 'Saved', _args[ 'filename' ] )

	if _args[ 'show' ]:
		plt.show()

	plt.close()

def plot_eclipse_array( ets, arr, args ):
	_args = {
		'figsize'          : ( 16, 8 ),
		'labels'           : [ '' ],
		'time_unit'        : 'seconds',
		'color'            : 'm',
		'lw'               : 2,
		'labelsize'        : 15,
		'legend_fontsize'  : 20,
		'legend_framealpha': 0.3,
		'title'            : 'Eclipse Array',
		'xlim'             : None,
		'legend'           : True,
		'show'             : False,
		'filename'         : False,
		'dpi'              : 300,
	}
	for key in args.keys():
		_args[ key ] = args[ key ]

	fig, ax0 = plt.subplots( 1, 1, figsize = _args[ 'figsize' ] )

	_args[ 'xlabel' ] = time_handler[ _args[ 'time_unit' ] ][ 'xlabel' ]
	time_coeff        = time_handler[ _args[ 'time_unit' ] ][ 'coeff'  ]

	_ets = ( ets - ets[ 0 ] ) / time_coeff

	if _args[ 'xlim' ] is None:
		_args[ 'xlim' ] = [ 0, _ets[ -1 ] ]

	ax0.plot( _ets, arr, '-o', color = _args[ 'color' ],
		linewidth = _args[ 'lw' ], ms = 5 )

	ax0.grid( linestyle = 'dotted' )
	ax0.set_xlim( _args[ 'xlim' ] )
	ax0.set_ylim( [ -1.5, 2.5 ] )
	ax0.set_xlabel( _args[ 'xlabel' ], size = _args[ 'labelsize' ] )
	ax0.set_ylabel( r'$1=Penumbra$, $2=Umbra$',
		size = _args[ 'labelsize' ] )

	plt.suptitle( _args[ 'title' ] )
	plt.tight_layout()

	if _args[ 'filename' ]:
		plt.savefig( _args[ 'filename' ], dpi = _args[ 'dpi' ] )
		print( 'Saved', _args[ 'filename' ] )

	if _args[ 'show' ]:
		plt.show()

	plt.close()

def plot_cr3bp_2d( mu, rs, args ):
	_args = {
		'figsize'      : ( 10, 10 ),
		'labels'       : [ '' ] * len( rs ),
		'colors'       : COLORS[ : ],
		'lw'           : 2.5,
		'hline_lstyles': 'dashed',
		'title'        : 'Trajectories',
		'legend'       : True,
		'show'         : False,
		'filename'     : False,
		'dpi'          : 300,
	}
	for key in args.keys():
		_args[ key ] = args[ key ]

	plt.figure( figsize = _args[ 'figsize' ] )
	plt.plot( -mu,    0, 'mo', ms = 10 )
	plt.plot( 1 - mu, 0, 'co', ms = 5  )

	n = 0
	for r in rs:
		plt.plot( r[ :, 0 ], r[ :, 1 ], _args[ 'colors' ][ n ],
			label = _args[ 'labels' ][ n ] )
		plt.plot( r[ 0, 0 ], r[ 0, 1 ], 'o',
			color = _args[ 'colors' ][ n ] )
		n += 1

	plt.grid( linestyle = 'dotted' )
	plt.title( _args[ 'title' ] )
	plt.tight_layout()

	if _args[ 'legend' ]:
		plt.legend( fontsize = 'large' )

	if _args[ 'filename' ]:
		plt.savefig( _args[ 'filename' ], dpi = _args[ 'dpi' ] )
		print( 'Saved', _args[ 'filename' ] )

	if _args[ 'show' ]:
		plt.show()

	plt.close()

def plot_cr3bp_3d( mu, rs, args, vectors = [] ):
	_args = {
		'figsize'      : ( 10, 8 ),
		'labels'       : [ '' ] * len( rs ),
		'colors'       : COLORS[ : ],
		'b1_ms'        : 7,
		'b2_ms'        : 5,
		'b1_color'     : 'm',
		'b2_color'     : 'c',
		'ALR'          : 0.03,
		'traj_lws'     : 1,
		'axes_mag'     : 0.8,
		'axes_custom'  : None,
		'legend'       : True,
		'axes_no_fill' : True,
		'hide_axes'    : False,
		'azimuth'      : False,
		'elevation'    : False,
		'show'         : False,
		'filename'     : False,
		'dpi'          : 300,
		'vector_colors': [ '' ] * len( vectors ),
		'vector_labels': [ '' ] * len( vectors ),
		'vector_texts' : False
	}
	for key in args.keys():
		_args[ key ] = args[ key ]

	fig = plt.figure( figsize = _args[ 'figsize' ] )
	ax  = fig.add_subplot( 111, projection = '3d'  )

	max_val = 0
	n       = 0

	for r in rs:
		ax.plot( r[ :, 0 ], r[ :, 1 ], r[ : , 2 ],
			color = _args[ 'colors' ][ n ], label = _args[ 'labels' ][ n ],
			zorder = 10, linewidth = _args[ 'traj_lws' ] )
		ax.plot( [ r[ 0, 0 ] ], [ r[ 0 , 1 ] ], [ r[ 0, 2 ] ], 'o',
			color = _args[ 'colors' ][ n ] )

		max_val = max( [ r.max(), max_val ] )
		n += 1

	ax.plot( [ -mu ], [ 0 ], [ 0 ], 'o',
		ms = _args[ 'b1_ms' ], color = _args[ 'b1_color' ] )
	ax.plot( [ 1 - mu ], [ 0 ], [ 0 ], 'o',
		ms = _args[ 'b2_ms' ], color = _args[ 'b2_color' ] )

	for vector in vectors:
		ax.quiver( 0, 0, 0,
			vector[ 'r' ][ 0 ], vector[ 'r' ][ 1 ], vector[ 'r' ][ 2 ],
			color = vector[ 'color' ], label = vector[ 'label' ] )

		if _args[ 'vector_texts' ]:
			vector[ 'r' ] *= _args[ 'vector_text_scale' ]
			ax.text( vector[ 'r' ][ 0 ], vector[ 'r' ][ 1 ], vector[ 'r' ][ 2 ],
				vector[ 'label' ],
				color = vector[ 'color' ] )

	ax_length = ( 1 - mu ) * 1.3
	ax.quiver( 0, 0, 0, ax_length, 0, 0, color = 'w',
		arrow_length_ratio = _args[ 'ALR' ], linewidth = 1 )
	ax.quiver( 0, 0, 0, 0, ax_length, 0, color = 'w',
		arrow_length_ratio = _args[ 'ALR' ], linewidth = 1 )
	ax.quiver( 0, 0, 0, 0, 0, ax_length, color = 'w',
		arrow_length_ratio = _args[ 'ALR' ], linewidth = 1 )

	if _args[ 'axes_custom' ] is not None:
		max_val = _args[ 'axes_custom' ]
	else:
		max_val *= _args[ 'axes_mag' ]

	ax.set_xlim( [ -max_val, max_val ] )
	ax.set_ylim( [ -max_val, max_val ] )
	ax.set_zlim( [ -max_val, max_val ] )
	ax.set_xlabel( 'X' )
	ax.set_ylabel( 'Y' )
	ax.set_zlabel( 'Z' )
	ax.set_box_aspect( [ 1, 1, 1 ] )
	ax.set_aspect( 'auto' )

	if _args[ 'azimuth' ] is not False:
		ax.view_init( elev = _args[ 'elevation' ],
					  azim = _args[ 'azimuth'   ] )

	if _args[ 'axes_no_fill' ]:
		ax.w_xaxis.pane.fill = False
		ax.w_yaxis.pane.fill = False
		ax.w_zaxis.pane.fill = False

	if _args[ 'hide_axes' ]:
		ax.set_axis_off()

	if _args[ 'legend' ]:
		plt.legend()

	if _args[ 'filename' ]:
		plt.savefig( _args[ 'filename' ], dpi = _args[ 'dpi' ] )
		print( 'Saved', _args[ 'filename' ] )

	if _args[ 'show' ]:
		plt.show()

	plt.close()

def cr3bp_pseudopotential( mu, r ):
	r13 = np.linalg.norm( [ r[ 0 ] + mu, r[ 1 ] ] )
	r23 = np.linalg.norm( [ r[ 0 ] - 1 + mu, r[ 1 ] ] )

	return ( 1 - mu ) / r13 + mu / r23 + 0.5 * ( r[ 0 ] ** 2 + r[ 1 ] ** 2 )

def plot_pseudopotential_contours( system, args ):
	_args = {
		'figsize'      : ( 10, 10 ),
		'LPs'          : True,
		'lw'           : 2.5,
		'clabels'      : False,
		'levels'       : None,
		'title'        : 'Trajectories',
		'legend'       : True,
		'show'         : False,
		'filename'     : False,
		'dpi'          : 300,
	}
	for key in args.keys():
		_args[ key ] = args[ key ]

	plt.figure( figsize = _args[ 'figsize' ] )
	plt.plot( -system[ 'mu' ],    0, 'mo', ms = 10 )
	plt.plot( 1 - system[ 'mu' ], 0, 'co', ms = 8  )

	if _args[ 'LPs' ]:
		plt.plot( system[ 'L1' ], 0, 'ro', ms = 7, label = 'L1' )
		plt.plot( system[ 'L2' ], 0, 'go', ms = 7, label = 'L2' )
		plt.plot( system[ 'L3' ], 0, 'bo', ms = 7, label = 'L3' )
		plt.plot( 0.5 - system[ 'mu' ], 3 ** 0.5 / 2.0,
			'co', ms = 7, label = 'L4' )
		plt.plot( 0.5 - system[ 'mu' ], -3 ** 0.5 / 2.0,
			'mo', ms = 7, label = 'L5' )

	x       = np.linspace( -1.3, 1.3, 200 )
	y       = np.linspace( -1.3, 1.3, 200 )
	n_vals  = len( x )
	omegas  = np.zeros( ( n_vals, n_vals ) )

	if _args[ 'levels' ] is None:
		levels0 = np.arange( 1, 2, 0.03 )
		levels1 = np.arange( 2, 7, 0.5 )
		levels2 = np.arange( 8, 10, 0.5 )
		levels  = np.concatenate( ( levels0, levels1, levels2 ) )
	else:
		levels = _args[ 'levels' ]

	for nx in range( n_vals ):
		for ny in range( n_vals ):
			omegas[ ny, nx ] = cr3bp_pseudopotential( system[ 'mu' ],
				[ x[ nx ], y[ ny ] ] )

	X, Y = np.meshgrid( x, y )
	cs   = plt.contour( X, Y, omegas, levels = levels )

	if _args[ 'clabels' ]:
		plt.clabel( cs, inline = 1 )

	plt.grid( linestyle = 'dotted' )
	plt.title( _args[ 'title' ] )
	plt.xticks( fontsize = 15 )
	plt.yticks( fontsize = 15 )
	plt.tight_layout()

	if _args[ 'legend' ]:
		plt.legend( fontsize = 'xx-large' )

	if _args[ 'filename' ]:
		plt.savefig( _args[ 'filename' ], dpi = _args[ 'dpi' ] )
		print( 'Saved', _args[ 'filename' ] )

	if _args[ 'show' ]:
		plt.show()

	plt.close()

