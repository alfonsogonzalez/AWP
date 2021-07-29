'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Lambert Solvers
'''

# Python standard libraries
import math

# 3rd party libraries
import numpy as np

# AWP libraries
import numerical_tools as nt
import planetary_data  as pd

def lamberts_universal_variables( r0, r1, deltat, args ):
	'''
	Solve Lambert's problem using universal variable method
	'''
	_args = {
		'tm'       : 1,
		'mu'       : pd.sun[ 'mu' ],
		'tol'      : 1e-6,
		'max_steps': 200,
		'psi'      : 0.0,
		'psi_u'    :  4.0 * math.pi ** 2,
		'psi_l'    : -4.0 * math.pi ** 2,
	}
	for key in args.keys():
		_args[ key ] = args[ key ]
	psi   = _args[ 'psi' ]
	psi_l = _args[ 'psi_l' ]
	psi_u = _args[ 'psi_u' ]

	sqrt_mu = math.sqrt( _args[ 'mu' ] )
	r0_norm = nt.norm( r0 )
	r1_norm = nt.norm( r1 )
	gamma   = np.dot( r0, r1 ) / r0_norm / r1_norm
	c2      = 0.5
	c3      = 1 / 6.0
	solved  = False
	A       = _args[ 'tm' ] * math.sqrt( r0_norm * r1_norm * ( 1 + gamma ) )

	if A == 0.0:
		raise RuntimeWarning(
			'Universal variables solution was passed in Hohmann transfer' )
		return np.array( [ 0, 0, 0 ] ), np.array( [ 0, 0, 0 ] )

	for n in range( _args[ 'max_steps' ] ):
		B = r0_norm + r1_norm + A * ( psi * c3 - 1 ) / math.sqrt( c2 )

		if A > 0.0 and B < 0.0:
			psi_l += math.pi
			B     *= -1.0

		chi3    = math.sqrt( B / c2 ) ** 3
		deltat_ = ( chi3 * c3 + A * math.sqrt( B ) ) / sqrt_mu

		if abs( deltat - deltat_ ) < _args[ 'tol' ]:
			solved = True
			break

		if deltat_ <= deltat:
			psi_l = psi

		else:
			psi_u = psi

		psi = ( psi_u + psi_l ) / 2.0
		c2  = C2( psi )
		c3  = C3( psi )

	if not solved:
		raise RuntimeWarning(
			'Universal variables solver did not converge.' )
		return np.array( [ 0, 0, 0 ] ), np.array( [ 0, 0, 0 ] )

	f    = 1 - B / r0_norm
	g    = A * math.sqrt( B / _args[ 'mu' ] )
	gdot = 1 - B / r1_norm
	v0   = ( r1 - f * r0 ) / g
	v1   = ( gdot * r1 - r0 ) / g

	return v0, v1

def C2( psi ):
	'''
	Stumpff function
	'''
	return ( 1 - math.cos( math.sqrt( psi ) ) ) / psi

def C3( psi ):
	'''
	Stumpff function
	'''
	sqrt_psi = math.sqrt( psi )
	return ( sqrt_psi - math.sin( sqrt_psi ) ) / ( psi * sqrt_psi )
