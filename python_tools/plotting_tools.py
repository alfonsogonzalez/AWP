'''
Astrodynamics with Python Plotting Tools
'''

import matplotlib.pyplot as plt
plt.style.use( 'dark_background' )

time_handler = {
	'seconds': { 'coeff': 1.0,        'xlabel': 'Time (seconds)' },
	'hours'  : { 'coeff': 3600.0,     'xlabel': 'Time (hours)'   },
	'days'   : { 'coeff': 86400.0,    'xlabel': 'Time (days)'    },
	'years'  : { 'coeff': 31536000.0, 'xlabel': 'Time (years)'   }
}

dist_handler = {
	'km': 1.0,
	'ER': 1 / 6378.0,
	'AU': 6.68459e-9
}

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
