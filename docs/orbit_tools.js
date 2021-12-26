/*
AID | Astrodynamics Interactive Demo with HTML/CSS/JavaScript, Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Orbital mechanics tools script
*/

function two_body_ode( t, y ) {
	r = y.slice( 0, 3 );
	a = scale( r, -CB[ 'mu' ] / Math.pow( norm( r ), 3 ) );
	return [ y[ 3 ], y[ 4 ], y[ 5 ], a[ 0 ], a[ 1 ], a[ 2 ] ];
}

function propagate_orbit( state, tspan, dt ) {
	n_steps     = Math.ceil( tspan / dt ) + 1;
	states      = Array( n_steps ).fill( Array( 6 ) );
	states[ 0 ] = state;

	for ( var n = 1; n < n_steps; n++ ) {
		states[ n ] = rk4_step( two_body_ode, n, states[ n - 1 ], dt );
	}
	return states;
}

function state2period( state ) {
	eps = Math.pow( norm( state.slice( 3, 6 ) ), 2 ) /
			2.0 - CB[ 'mu' ] / norm( state.slice( 0, 3 ) );
	sma = -CB[ 'mu' ] / ( 2.0 * eps );
	return 2 * Math.PI * Math.sqrt( Math.pow( sma, 3 ) / CB[ 'mu' ] );
}

function perif2eci( raan, aop, inc ) {
	matrix = math.multiply( Cz( raan ), Cx( inc ) );
	return math.multiply( matrix, Cz( aop ) );
}

function tae2E( ta, ecc ) {
	return 2 * Math.atan(
		Math.sqrt( ( 1 - ecc ) / ( 1 + ecc ) ) *
		Math.tan( ta / 2 ) );
}

function coes2state( coes ) {
	let [ sma, ecc, inc, ta, aop, raan ] = coes;
	sta     = Math.sin( ta );
	cta     = Math.cos( ta );
	p       = sma * ( 1 - Math.pow( ecc, 2 ) );
	r_norm  = p / ( 1 + ecc * cta );
	r_perif = math.multiply( math.matrix( [ cta, sta, 0 ] ), r_norm );
	v_perif = math.multiply( math.matrix( [ -sta, ecc + cta, 0 ] ),
					 Math.sqrt( CB[ 'mu' ] / p ) );
	matrix  = perif2eci( raan, aop, inc );
	r_ECI   = math.multiply( matrix, r_perif );
	v_ECI   = math.multiply( matrix, v_perif );
	return math.concat( r_ECI, v_ECI ).valueOf();
}
