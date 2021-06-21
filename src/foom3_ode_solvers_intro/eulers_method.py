'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Fundamentals of Orbital Mechanics 3
Ordinary Differential Equations (ODEs) Solvers Introduction

Visualize how Euler's method for solving
ordinary differential equations (ODEs) works
'''

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'dark_background' )

def euler_step( df, x, h ):
	'''
	Implementation of 1 step of euler's method
	'''
	return df( x ) * h

def df( x ):
	'''
	Derivative of function f'( x ) = x
	'''
	return x

def f( x ):
	'''
	Function f( x ) = x^2 / 2
	'''
	return x ** 2 / 2.0

if __name__ == '__main__':
	h             = 0.2                      # step size
	xs            = np.arange( 0, 5 + h, h ) # independent variable x
	n_steps       = len( xs )                # number of steps
	ys_analytical = f( xs )                  # analytical solution to df/dx
	ys_euler      = np.zeros( n_steps )      # empty array, initial condition:
	                                         # f( 0 ) = 0
	for n in range( 1, n_steps ):
		ys_euler[ n ] = euler_step( df, xs[ n - 1 ], h ) + ys_euler[ n - 1 ]
	errors = ys_euler - ys_analytical

	plt.figure( figsize = ( 16, 8 ) )
	plt.plot( xs, ys_analytical, 'm', label = 'Analytical Solution' )
	plt.plot( xs, ys_euler,      'c', label = 'Euler\'s Method Solution' )
	plt.plot( xs, ys_euler,      'co' )
	plt.plot( xs, errors,        'r', label = 'Euler\'s Method Error' )
	plt.plot( xs, errors,        'ro' )
	plt.grid( linestyle = 'dotted' )
	plt.xlabel( r'$x$' )
	plt.ylabel( r'$f$' )
	plt.legend( prop = { 'size': 15 } )

	title  = 'Euler\'s Method to Solve:  '
	title += r'$\dfrac{df}{dx}=x$,    '
	title += r'Solution: $f( x ) = \dfrac{x^2}{2}$'
	plt.title( title, fontsize = 15 )
	plt.show()