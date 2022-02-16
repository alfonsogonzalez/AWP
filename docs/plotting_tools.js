/*
AID | Astrodynamics Interactive Demo with HTML/CSS/JavaScript, Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Plotting tools
*/

const COLORS                 = [ 'magenta', 'cyan', 'lime', 'red' ];
const VINF_COLOR             = 'gold';
const BASIS_VECTORS_SCALE    = 2.0;
const MAX_VAL_SCALE          = 2.5;
const GROUNDTRACK_MARKERSIZE = 2;
const RV_LINEWIDTH           = 3;
const EQ_PLANE_OPACITY       = 0.7;

function make_basis_vectors( radius ) {
	return [
		{
			x: [ 0, radius * BASIS_VECTORS_SCALE ], y: [ 0, 0 ], z: [ 0, 0 ],
			mode: 'lines+markers', line: { color: 'white', width: 5 },
			type: 'scatter3d', marker: { size: 5, color: 'red' }, name: 'X'
		},
		{
			x: [ 0, 0 ], y: [ 0, radius * BASIS_VECTORS_SCALE ], z: [ 0, 0 ],
			mode: 'lines+markers', line: { color: 'white', width: 5 },
			type: 'scatter3d', marker: { size: 5, color: 'green' }, name: 'Y'
		},
		{
			x: [ 0, 0 ], y: [ 0, 0 ], z: [ 0, radius * BASIS_VECTORS_SCALE ],
			mode: 'lines+markers', line: { color: 'white', width: 5 },
			type: 'scatter3d', marker: { size: 5, color: 'blue' }, name: 'Z'
		}
	]
}

function make_sphere( radius ) {
	xx    = [];
	yy    = [];
	zz    = [];
	phi   = linspace( 0,     Math.PI / 2, 15 );  
	theta = linspace( 0, 2 * Math.PI,     15 ); 

	for ( i = 0; i < theta.length; i++ ) {
	    for ( j = 0; j < phi.length; j++ ){
	        xx.push( Math.cos( theta[ i ] ) * Math.sin( phi[ j ] ) );
	        yy.push( Math.sin( theta[ i ] ) * Math.sin( phi[ j ] ) );   
	        zz.push( Math.cos( phi[ j ] ) );
	    }
	}
	xx = scale( xx, radius );
	yy = scale( yy, radius );
	zz = scale( zz, radius );

	const dataitem = {
	    x: xx, y: yy, z: zz,
	    opacity: 0.5,
	    color  : CB[ 'color' ],
	    type   : 'mesh3d',
	}
	var data = [
	    dataitem,
	    { ...dataitem, z: zz.map( v => -v ) }
	];
	return data;
}

function make_trace_3d( states, n, max_val ) {
	rx      = states.map( function( a ){ return a[ 0 ] } );
	ry      = states.map( function( a ){ return a[ 1 ] } );
	rz      = states.map( function( a ){ return a[ 2 ] } );
	max_x   = Math.max( ...rx.map( a => Math.abs( a ) ) );
	max_y   = Math.max( ...ry.map( a => Math.abs( a ) ) );
	max_z   = Math.max( ...rz.map( a => Math.abs( a ) ) );
	max_val = Math.max( max_x, max_y, max_z, max_val );

	return [ {
	  x     : rx, y : ry, z : rz,
	  mode  : 'lines',
	  line  : {
	    color: COLORS[ n ],
	    width: 4
	  },
	  type: 'scatter3d',
	  name: 'Orbit ' + n
	}, max_val ];
}

function make_trace_gt( latlons, n ) {
	return {
		x     : latlons.map( function( a ) { return a[ 1 ] } ),
		y     : latlons.map( function( a ) { return a[ 2 ] } ),
		mode  : 'markers',
		name  : 'Orbit' + n,
		marker: { color: COLORS[ n ], size: GROUNDTRACK_MARKERSIZE },
		type  : 'scatter',
	};	
}

function make_trace_rv( ets, states, n ) {
	rnorms = states.map( function ( a ) {
		return norm( [ a[ 0 ], a[ 1 ], a[ 2 ] ] ) } );
	vnorms = states.map( function ( a ) {
		return norm( [ a[ 3 ], a[ 4 ], a[ 5 ] ] ) } );
	ts     = ets.map( function ( a ) { return a / 3600.0 } );
	return [ {
		x    : ts,
		y    : vnorms,
		mode : 'lines',
		name : 'Orbit' + n,
		line : { color: COLORS[ n ], width: RV_LINEWIDTH },
		type : 'scatter',
		xaxis: 'x2',
		yaxis: 'y2'
	},
	{
		x   : ts,
		y   : rnorms,
		mode: 'lines',
		name: 'Orbit' + n,
		line: { color: COLORS[ n ], width: RV_LINEWIDTH },
		type: 'scatter',
	} ];	
}

function make_trace_rv_vinf( xmax, vinf ) {
	return {
		x    : [ 0, xmax ],
		y    : [ vinf, vinf ],
		mode : 'lines',
		name : 'vinf',
		line : { color: VINF_COLOR, width: RV_LINEWIDTH },
		type : 'scatter',
		xaxis: 'x2',
		yaxis: 'y2'
	};
}

function make_trace_eq_plane( max_val ) {
	return {
		x         : [ [ max_val,  max_val ], [ -max_val, -max_val ] ],
		y         : [ [ max_val, -max_val ], [  max_val, -max_val ] ],
		z         : [ [ 0, 0 ], [ 0, 0 ] ],
		type      : 'surface',
		opacity   : EQ_PLANE_OPACITY,
		colorscale: 'Blues',
		showscale : false
	}
}

function make_trace_vec( v, n, ccolor = false ) {
	let mag = CB[ 'radius' ] * BASIS_VECTORS_SCALE;

	if ( ccolor ) { _color = VINF_COLOR; }
	else { _color = COLORS[ n ]; }

	return {
		x: [ 0, v[ 0 ] * mag ], y: [ 0, v[ 1 ] * mag ], z: [ 0, v[ 2 ] * mag ],
		mode  : 'lines+markers',
		line  : { color: _color, width: 5 },
		type  : 'scatter3d',
		marker: { size: 5, color: _color }, name: 'h'
	}
}

function create_3d_plot( states_list, hs_list, idxs, lims = false ) {
	let traces  = [];
	let max_val = 0;
	for( var n = 0; n < idxs.length; n++ ) {
		vals    = make_trace_3d( states_list[ n ], idxs[ n ], max_val );
		max_val = Math.max( max_val, vals[ 1 ] );
		traces.push( vals[ 0 ] );
		if ( hs_checkbox.checked ) {
			traces.push( make_trace_vec( hs_list[ n ], idxs[ n ] ) );
		}
	}
	if ( lims ) { max_val = lims; }
	else { max_val *= MAX_VAL_SCALE; }

	sphere_data   = make_sphere( CB[ 'radius' ] );
	basis_vectors = make_basis_vectors( CB[ 'radius' ] );
	traces.push( sphere_data[ 0 ] );
	traces.push( sphere_data[ 1 ] );
	traces.push( basis_vectors[ 0 ] );
	traces.push( basis_vectors[ 1 ] );
	traces.push( basis_vectors[ 2 ] );

	if ( eq_plane_checkbox.checked ) {
		traces.push( make_trace_eq_plane( max_val ) );
	}

	if ( vinf_checkbox.checked ) {
		let vinf        = read_vinf();
		let vinf_normed = scale( vinf, 1 / norm( vinf ) );
		traces.push( make_trace_vec( vinf_normed, 0, true ) );
	}

	let layout = {
	  title        : false,
	  showlegend   : false,
	  autosize     : false,
	  width        : 500,
	  height       : 500,
	  bgcolor      : ( 0, 0, 0 ),
	  margin       : { l: 0, r: 0, b: 0, t: 65 },
	  plot_bgcolor : "black",
	  paper_bgcolor: "#0000",
	  scene        : {
		  xaxis: { range: [ -max_val, max_val ] },
		  yaxis: { range: [ -max_val, max_val ] },
		  zaxis: { range: [ -max_val, max_val ] },
		  aspectratio: { x: 1, y: 1, z: 1 }
		}
	};

	Plotly.newPlot( 'plot-3d', traces, layout );	
}

function create_groundtracks_plot( latlons_list, idxs ) {
	var layout_gt = {
		title: false,
		xaxis: {
			range    : [ -180, 180 ],
			autorange: false,
			tickmode : 'linear',
			tick0    : -180,
			dtick    : 30,
			title    : 'Longitude'
		},
		yaxis: {
			range    : [ -90,  90  ],
			autorange: false,
			tickmode : 'linear',
			tick0    : -90,
			dtick    : 30,
			title    : 'Latitude'
		},
		plot_bgcolor : 'black',
		paper_bgcolor: '#0000',
		images       : [ {
			source: CB[ 'img' ],
			xref  : 'x', yref: 'y',
			x     : -180, y: 90,
			sizex : 360, sizey: 180,
			sizing: 'stretch',
			layer : 'below'
		} ],
		margin: { l: 50, r: 50, b: 50, t: 0, pad: 1 },
		showlegend: false
	};

	var traces_gt = []
	for( var n = 0; n < idxs.length; n++ ) {
		traces_gt.push( make_trace_gt( latlons_list[ n ], idxs[ n ] ) );
	}
	Plotly.newPlot( 'plot-groundtracks', traces_gt, layout_gt );
}

function create_rv_plot( ets_list, states_list, idxs, xlim = false, ylims = false ) {
	var traces_rv = []
	var xmax      = 0;
	var rmax      = 0;
	var vmax      = 0;
	for( var n = 0; n < idxs.length; n++ ) {
		traces = make_trace_rv( ets_list[ n ], states_list[ n ], idxs[ n ] );
		traces_rv.push( traces[ 0 ] );
		traces_rv.push( traces[ 1 ] );
		xmax  = Math.max( xmax, ets_list[ n ][ ets_list[ n ].length - 1 ] / 3600.0 );
		rmax  = Math.max( rmax, Math.max.apply( Math, traces[ 1 ][ 'y' ] ) );
		vmax  = Math.max( vmax, Math.max.apply( Math, traces[ 0 ][ 'y' ] ) );
	}
	if ( xlim  ) { xmax = xlim; }
	if ( ylims ) { rmax = ylims[ 0 ]; vmax = ylims[ 1 ]; }

	if ( vinf_checkbox.checked ) {
		let vinf = read_vinf();
		traces_rv.push( make_trace_rv_vinf( xmax, norm( vinf ) ) );
	}

	var layout_rv = {
		title        : false,
		showlegend   : false,
		plot_bgcolor : 'black',
		paper_bgcolor: '#0000',
		margin       : { l: 50, r: 50, b: 50, t: 50, pad: 1 },
		grid         : {
			rows: 2, columns: 1, pattern: 'independent', roworder: 'bottom to top'
		},
		xaxis1: { title: "Time (hours)", showgrid: true, gridcolor: 'white',
				  range: [ 0, xmax ], autorange: false },
		xaxis2: { showgrid: true, gridcolor: 'white',
				  range: [ 0, xmax ], autorange: false },
		yaxis1: { title: "Position (km)", showgrid: true, gridcolor: 'white',
				  range: [ CB[ 'radius' ], rmax ], autorange: false },
		yaxis2: { title: "Velocity (km/s)", showgrid: true, gridcolor: 'white',
				  range: [ 0, vmax ], autorange: false }
	};

	Plotly.newPlot( 'plot-positions-velocities', traces_rv, layout_rv );
}
