/*
AID | Astrodynamics Interactive Demo with HTML/CSS/JavaScript, Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Ordinary Differential Equation (ODE) tools script
*/

function euler_step( f, t, y, h ) {
	dy = f( t, y );
	return add( y, scale( dy, h ) );
}

function rk4_step( f, t, y, h ) {
	let k1    = f( t, y )
	let k2    = f( t + 0.5 * h, add( y, scale( k1, 0.5 * h ) ) );
	let k3    = f( t + 0.5 * h, add( y, scale( k2, 0.5 * h ) ) );
	let k4    = f( t +       h, add( y, scale( k3, h ) ) );
	var wmean = add( k1, scale( k2, 2 ) );
	wmean     = add( wmean, scale( k3, 2 ) );
	wmean     = add( wmean, k4 );
	wmean     = scale( wmean, h / 6 );
	return add( y, wmean );
}
