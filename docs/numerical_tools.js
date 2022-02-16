/*
AID | Astrodynamics Interactive Demo with HTML/CSS/JavaScript, Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Numerical tools script
*/

d2r = Math.PI / 180.0;
r2d = 180.0 / Math.PI;

REFERENCE_FRAME_MAP = {
	'IAU_EARTH': eci2ecef,
	'IAU_MOON' : mci2mcmf,
	'IAU_MARS' : maci2macmaf
}

function add( v0, v1 ) {
	a = Array( v0.length );
	for ( var n = 0; n < v0.length; n++ ) {
		a[ n ] = v0[ n ] + v1[ n ];
	}
	return a;
}

function mult( v0, v1 ) {
	a = Array( v0.length );
	for ( var n = 0; n < v0.length; n++ ) {
		a[ n ] = v0[ n ] * v1[ n ];
	}
	return a;
}

function scale( v0, v1 ) {
	a = Array( v0.length );
	for ( var n = 0; n < v0.length; n++ ) {
		a[ n ] = v0[ n ] * v1;
	}
	return a;
}

function norm( v ) {
	sum = 0;
	for ( var n = 0; n < v.length; n++ ){
		sum += v[ n ] * v[ n ];
	}
	return Math.sqrt( sum );
}

function cross( v0, v1 ) {
	return [
		v0[ 1 ] * v1[ 2 ] - v0[ 2 ] * v1[ 1 ],
		v0[ 2 ] * v1[ 0 ] - v0[ 0 ] * v1[ 2 ],
		v0[ 0 ] * v1[ 1 ] - v0[ 1 ] * v1[ 0 ]
	]
}

function linspace( start, stop, n ) {
    var arr  = [];
    var step = ( stop - start ) / ( n - 1 );
    for ( var i = 0; i < n; i++ ) {
      arr.push( start + ( step * i ) );
    }
    return arr;
}

function Cx( a ) {
	sa = Math.sin( a );
	ca = Math.cos( a );
	return math.matrix( [ 
		[ 1,  0,   0 ],
		[ 0, ca, -sa ],
		[ 0, sa,  ca ]
	] )
}

function Cy( a ) {
	sa = Math.sin( a );
	ca = Math.cos( a );
	return math.matrix( [
		[  ca, 0, sa ],
		[   0, 1,  0 ],
		[ -sa, 0, ca ]
	] )
}

function Cz( a ) {
	sa = Math.sin( a );
	ca = Math.cos( a );
	return math.matrix( [ 
		[ ca, -sa, 0 ],
		[ sa,  ca, 0 ],
		[  0,   0, 1 ]
	] )
}

function frame_transform( arrs, from, to, ets ) {
	out  = Array( ets.length ).fill( Array( 3 ) );
	func = REFERENCE_FRAME_MAP[ to ];
	for ( var n = 0; n < ets.length; n++ ) {
		out[ n ] = math.multiply(
			func( ets[ n ] ), arrs[ n ] ).valueOf();
	}
	return out;
}

function eci2ecef( et ) {
	return Cz( -EARTH[ 'omega' ] * et );
}

function mci2mcmf( et ) {
	return Cz( -MOON[ 'omega' ] * et );
}

function maci2macmaf( et ) {
	return Cz( -MARS[ 'omega' ] * et );
}

function reclat( r ) {
	rnorm = norm( r );
	return [
		rnorm,
		Math.atan2( r[ 1 ], r[ 0 ] ),
		Math.asin( r[ 2 ] / rnorm )
	]
}

function cart2lat( rs, from, to, ets ) {
	rs_bf   = frame_transform( rs, from, to, ets );
	latlons = Array( ets.length ).fill( Array( 3 ) );
	for ( var n = 0; n < ets.length; n++ ) {
		latlons[ n ]       = reclat( rs_bf[ n ].valueOf() );
		latlons[ n ][ 1 ] *= r2d;
		latlons[ n ][ 2 ] *= r2d;
	}
	return latlons;
}