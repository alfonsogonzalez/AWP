/*
AID | Astrodynamics Interactive Demo with HTML/CSS/JavaScript, Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

main script
*/

const propagate_button  = document.getElementById( "propagate_button" );
const animate_button    = document.getElementById( "animate_button" );
const hs_checkbox       = document.getElementById( 'hs-checkbox' );
const eq_plane_checkbox = document.getElementById( 'active-eq-plane' );
const vinf_checkbox     = document.getElementById( 'vinf-checkbox' );
const vinf_input_x      = document.getElementById( 'vinf-input-x' );
const vinf_input_y      = document.getElementById( 'vinf-input-y' );
const vinf_input_z      = document.getElementById( 'vinf-input-z' );

propagate_button.addEventListener( "click", create_stationary_plots );
animate_button.addEventListener( "click", create_animated_plots );

const N_STATE_VECTOR_INPUTS  = 2;
const N_COES_INPUTS          = 2;
const N_TOTAL_ORBITS         = N_STATE_VECTOR_INPUTS + N_COES_INPUTS;
const HYPERBOLIC_TSPAN       = 35000;

var CB = EARTH;
set_defaults();

function open_dropdown() {
	document.getElementById( 'dropdown' ).classList.toggle( 'show' );
}

window.onclick = function( event ) {
  if ( !event.target.matches( '.dropbtn' ) ) {
    var dropdowns = document.getElementsByClassName( 'dropdown-content' );
    for ( var n = 0; n < dropdowns.length; n++ ) {
      var openDropdown = dropdowns[ n ];
      if ( openDropdown.classList.contains( 'show' ) ) {
        openDropdown.classList.remove( 'show' );
      }
    }
  }
}

function set_central_body_earth() {
	CB = EARTH;
	set_defaults();
	create_stationary_plots();
}

function set_central_body_mars() {
	CB = MARS;
	set_defaults();
	create_stationary_plots();
}

function set_central_body_moon() {
	CB = MOON;
	set_defaults();
	create_stationary_plots();
}

function set_defaults() {
	for( var n = 0; n < N_STATE_VECTOR_INPUTS; n++ ) {
		document.getElementById( "rx" + n ).value = CB[ 'defaults' ][ 'rx' + n ];
		document.getElementById( "ry" + n ).value = CB[ 'defaults' ][ 'ry' + n ];
		document.getElementById( "rz" + n ).value = CB[ 'defaults' ][ 'rz' + n ];
		document.getElementById( "vx" + n ).value = CB[ 'defaults' ][ 'vx' + n ];
		document.getElementById( "vy" + n ).value = CB[ 'defaults' ][ 'vy' + n ];
		document.getElementById( "vz" + n ).value = CB[ 'defaults' ][ 'vz' + n ];
		document.getElementById( "dt" + n ).value = CB[ 'defaults' ][ 'dt' + n ];
		document.getElementById( "sim-time" + n ).value = CB[ 'defaults' ][ 'sim-time' + n ];
	}
	for( var n = 0; n < N_COES_INPUTS; n++ ) {
		document.getElementById( "sma"  + n ).value = CB[ 'defaults' ][ 'sma'  + n ];
		document.getElementById( "ecc"  + n ).value = CB[ 'defaults' ][ 'ecc'  + n ];
		document.getElementById( "inc"  + n ).value = CB[ 'defaults' ][ 'inc'  + n ];
		document.getElementById( "ta"   + n ).value = CB[ 'defaults' ][ 'ta'   + n ];
		document.getElementById( "aop"  + n ).value = CB[ 'defaults' ][ 'aop'  + n ];
		document.getElementById( "raan" + n ).value = CB[ 'defaults' ][ 'raan' + n ];
		document.getElementById( "dt-k" + n ).value = CB[ 'defaults' ][ 'dt-k' + n ];
		document.getElementById( "sim-time-k" + n ).value = CB[ 'defaults' ][ 'sim-time-k' + n ];
	}
}

function read_vinf() {
	return [
		parseFloat( vinf_input_x.value ),
		parseFloat( vinf_input_y.value ),
		parseFloat( vinf_input_z.value )
	];
}

function propagate_orbits() {
	let states_list  = [];
	let latlons_list = [];
	let ets_list     = [];
	let hs_list      = [];
	let n_orbit      = 0;
	let idxs         = [];

	for( var n = 0; n < N_STATE_VECTOR_INPUTS; n++ ) {
		if ( document.getElementById( 'active' + n ).checked ) {
			rx = parseFloat( document.getElementById( "rx" + n ).value );
			ry = parseFloat( document.getElementById( "ry" + n ).value );
			rz = parseFloat( document.getElementById( "rz" + n ).value );
			vx = parseFloat( document.getElementById( "vx" + n ).value );
			vy = parseFloat( document.getElementById( "vy" + n ).value );
			vz = parseFloat( document.getElementById( "vz" + n ).value );
			dt = parseFloat( document.getElementById( "dt" + n ).value );
			state   = [ rx, ry, rz, vx, vy, vz ];
			simtime = parseFloat( document.getElementById( "sim-time" + n ).value );
			tspan   = state2period( state ) * simtime;

			if ( isNaN( tspan ) ) {
				if ( simtime < 50 ) {
					tspan = HYPERBOLIC_TSPAN;
				}
				else { tspan = simtime; }
			}
			states  = propagate_orbit( state, tspan, dt )
			ets     = linspace( 0, tspan, states.length );
			latlons = cart2lat( states.map(
				function( a ){ return [ a[ 0 ], a[ 1 ], a[ 2 ] ] } ),
				'J2000', CB[ 'frame' ], ets );

			states_list.push( states );
			latlons_list.push( latlons );
			ets_list.push( ets );
			idxs.push( n_orbit );

			if ( hs_checkbox.checked ) {
				let hvec  = cross( [ rx, ry, rz ], [ vx, vy, vz ] );
				let hnorm = norm( hvec );
				hs_list.push( scale( hvec, 1 / hnorm ) );
			}
		}
		n_orbit++;
	}

	for( var n = 0; n < N_COES_INPUTS; n++ ) {
		if ( document.getElementById( 'active-k' + n ).checked ) {
			sma   = parseFloat( document.getElementById( "sma"  + n ).value );
			ecc   = parseFloat( document.getElementById( "ecc"  + n ).value );
			inc   = parseFloat( document.getElementById( "inc"  + n ).value );
			ta    = parseFloat( document.getElementById( "ta"   + n ).value );
			aop   = parseFloat( document.getElementById( "aop"  + n ).value );
			raan  = parseFloat( document.getElementById( "raan" + n ).value );
			dt    = parseFloat( document.getElementById( "dt-k" + n ).value );
			state = coes2state( [ sma, ecc, inc * d2r, ta * d2r, aop * d2r, raan * d2r ] );
			tspan = state2period( state.valueOf() ) *
				parseFloat( document.getElementById( "sim-time-k" + n ).value );
			states  = propagate_orbit( state, tspan, dt )
			ets     = linspace( 0, tspan, states.length );
			latlons = cart2lat( states.map(
				function( a ){ return [ a[ 0 ], a[ 1 ], a[ 2 ] ] } ),
				'J2000', CB[ 'frame' ], ets );

			states_list.push( states );
			latlons_list.push( latlons );
			ets_list.push( ets );
			idxs.push( n_orbit );

			if ( hs_checkbox.checked ) {
				let hvec  = cross( state.slice( 0, 3 ), state.slice( 3 ) );
				let hnorm = norm( hvec );
				hs_list.push( scale( hvec, 1 / hnorm ) );
			}
		}
		n_orbit++;
	}

	return [ ets_list, states_list, latlons_list, hs_list, idxs ];
}

function create_stationary_plots() {
	let [ ets_list, states_list, latlons_list, hs_list, idxs ] = propagate_orbits();
	create_3d_plot( states_list, hs_list, idxs );
	create_groundtracks_plot( latlons_list, idxs );
	create_rv_plot( ets_list, states_list, idxs );
}

function create_animated_plots() {
	let [ ets_list, states_list, latlons_list, idxs ] = propagate_orbits();

	var initial_states  = [];
	var initial_latlons = [];
	var rnorms_list     = [];
	var vnorms_list     = [];
	var et_max          = 0;
	var rmax            = 0;
	var vmax            = 0;

	for( var n = 0; n < idxs.length; n++ ) {
		initial_states.push( states_list[ n ][ 0 ] );
		initial_latlons.push( latlons_list[ n ][ 0 ] );

		rnorms = states_list[ n ].map( function ( a ) {
			return norm( [ a[ 0 ], a[ 1 ], a[ 2 ] ] ) } );
		vnorms = states_list[ n ].map( function ( a ) {
			return norm( [ a[ 3 ], a[ 4 ], a[ 5 ] ] ) } );

		rnorms_list.push( rnorms );
		vnorms_list.push( vnorms );
		et_max = Math.max(
			et_max, ets_list[ n ][ ets_list[ n ].length - 1 ] / 3600.0 );
		rmax = Math.max( rmax, Math.max.apply( Math, rnorms ) );
		vmax = Math.max( vmax, Math.max.apply( Math, vnorms ) );

	}

	create_3d_plot( initial_states, idxs, rmax );
	create_groundtracks_plot( initial_latlons, idxs );
	create_rv_plot( ets_list, initial_states, idxs, et_max, [ rmax, vmax ] );

	var step = 1;

	var interval_id = setInterval( function() {
		var xs     = [];
		var ys     = [];
		var zs     = [];
		var lats   = [];
		var lons   = [];
		var rvys   = [];
		var ets    = [];
		var rv_traces  = [];
		var trace_idxs = [];

		var rv_idx = 0;
		for( var idx = 0; idx < idxs.length; idx++ ) {
			try {
				xs.push( [ states_list[ idx ][ step ][ 0 ] ] );
				ys.push( [ states_list[ idx ][ step ][ 1 ] ] );
				zs.push( [ states_list[ idx ][ step ][ 2 ] ] );
				lats.push( [ latlons_list[ idx ][ step ][ 2 ] ] );
				lons.push( [ latlons_list[ idx ][ step ][ 1 ] ] );

				rvys.push( [ vnorms_list[ idx ][ step ] ] );
				rvys.push( [ rnorms_list[ idx ][ step ] ] );
				ets.push( [ ets_list[ idx ][ step ] / 3600.0 ] );
				ets.push( [ ets_list[ idx ][ step ] / 3600.0 ] );

				trace_idxs.push( idx );
				rv_traces.push( rv_idx );
				rv_traces.push( rv_idx + 1 );
			}
			catch {}
			rv_idx += 2;
		}

		Plotly.extendTraces( 'plot-3d', {
			x: xs, y: ys, z: zs }, trace_idxs );

		Plotly.extendTraces( 'plot-groundtracks', {
			x: lons, y: lats }, trace_idxs );

		Plotly.extendTraces( 'plot-positions-velocities', {
			x: ets, y: rvys	}, rv_traces );

		step++;

		if ( step >= states_list[ 1 ].length ) {
			clearInterval( interval_id );
		}
	}, 2 );
}

create_stationary_plots();
