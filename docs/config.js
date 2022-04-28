/*
AID | Astrodynamics Interactive Demo with HTML/CSS/JavaScript, Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Config script
*/

function read_state() {
	var config         = {};
	config[ 'planet' ] = CB[ 'name' ];
	
	for( var n = 0; n < N_STATE_VECTOR_INPUTS; n++ ) {
		config[ "rx" + n ] = document.getElementById( "rx" + n ).value;
		config[ "ry" + n ] = document.getElementById( "ry" + n ).value;
		config[ "rz" + n ] = document.getElementById( "rz" + n ).value;
		config[ "vx" + n ] = document.getElementById( "vx" + n ).value;
		config[ "vy" + n ] = document.getElementById( "vy" + n ).value;
		config[ "vz" + n ] = document.getElementById( "vz" + n ).value;
		config[ "dt" + n ] = document.getElementById( "dt" + n ).value;
		config[ "sim-time" + n ] = document.getElementById( "sim-time" + n ).value;
		config[ "active"   + n ] = document.getElementById( 'active'   + n ).checked;
	}
	for( var n = 0; n < N_COES_INPUTS; n++ ) {
		config[ "sma"  + n ] = document.getElementById( "sma"  + n ).value;
		config[ "ecc"  + n ] = document.getElementById( "ecc"  + n ).value;
		config[ "inc"  + n ] = document.getElementById( "inc"  + n ).value;
		config[ "ta"   + n ] = document.getElementById( "ta"   + n ).value;
		config[ "aop"  + n ] = document.getElementById( "aop"  + n ).value;
		config[ "raan" + n ] = document.getElementById( "raan" + n ).value;
		config[ "dt-k" + n ] = document.getElementById( "dt-k" + n ).value;
		config[ "sim-time-k" + n ] = document.getElementById( "sim-time-k" + n ).value;
		config[ "active-k"   + n ] = document.getElementById( 'active-k'   + n ).checked;
	}

	config[ "hs-checkbox"   ] = hs_checkbox.checked;
	config[ "vinf-checkbox" ] = vinf_checkbox.checked;

	vinf = read_vinf();
	config[ "vinf-x" ] = vinf[ 0 ];
	config[ "vinf-y" ] = vinf[ 1 ];
	config[ "vinf-z" ] = vinf[ 2 ];

	return config;
}

function write_text_box() {
	const config = read_state();
	read_config_text_box.innerHTML = JSON.stringify( config, undefined, 4 );
}

function read_text_box( type ) {
	if( type == "read" ) {
		return JSON.parse( read_config_text_box.value );
	}
	else if( type == "write" ) {
		return JSON.parse( write_config_text_box.value );
	}
	
}

function apply_config( config ) {
	CB = PLANETS[ config[ 'planet' ] ];
	for( var n = 0; n < N_STATE_VECTOR_INPUTS; n++ ) {
		document.getElementById( "rx" + n ).value = config[ 'rx' + n ];
		document.getElementById( "ry" + n ).value = config[ 'ry' + n ];
		document.getElementById( "rz" + n ).value = config[ 'rz' + n ];
		document.getElementById( "vx" + n ).value = config[ 'vx' + n ];
		document.getElementById( "vy" + n ).value = config[ 'vy' + n ];
		document.getElementById( "vz" + n ).value = config[ 'vz' + n ];
		document.getElementById( "dt" + n ).value = config[ 'dt' + n ];
		document.getElementById( "sim-time" + n ).value = config[ 'sim-time' + n ];
		document.getElementById( 'active' + n ).checked = config[ 'active' + n ];
	}
	for( var n = 0; n < N_COES_INPUTS; n++ ) {
		document.getElementById( "sma"  + n ).value = config[ 'sma'  + n ];
		document.getElementById( "ecc"  + n ).value = config[ 'ecc'  + n ];
		document.getElementById( "inc"  + n ).value = config[ 'inc'  + n ];
		document.getElementById( "ta"   + n ).value = config[ 'ta'   + n ];
		document.getElementById( "aop"  + n ).value = config[ 'aop'  + n ];
		document.getElementById( "raan" + n ).value = config[ 'raan' + n ];
		document.getElementById( "dt-k" + n ).value = config[ 'dt-k' + n ];
		document.getElementById( "sim-time-k" + n ).value = config[ 'sim-time-k' + n ];
		document.getElementById( 'active-k' + n ).checked = config[ 'active-k' + n ];
	}
	hs_checkbox.checked   = config[ "hs-checkbox"   ];
	vinf_checkbox.checked = config[ "vinf-checkbox" ];

	vinf_input_x.value = config[ "vinf-x" ];
	vinf_input_y.value = config[ "vinf-y" ];
	vinf_input_z.value = config[ "vinf-z" ];
}

function apply_written_config() {
	apply_config( read_text_box( "write" ) );
	create_stationary_plots();
}

function apply_default_config( n ) {
	const config = DEFAULT_CONFIGS[ n ];
	apply_config( config );
	create_stationary_plots();
}
