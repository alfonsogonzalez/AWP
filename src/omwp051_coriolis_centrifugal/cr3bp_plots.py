'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Create CR3BP plots
'''

# AWP library
from CR3BP import CR3BP

if __name__ == '__main__':
	states = [
		[ 1.2, 0, 0, 0, -0.71407169828407848921, 0 ],
		[ 1.2, 0, 0, 0, -0.67985320356540547720, 0 ],
		[ 1.2, 0, 0, 0, -0.66975741517271092087, 0 ]
	]
	tspans = [ 0.18337451820715063383e2, 0.30753758552140629263e2,
			   0.68127906604713772763e2 ]
	ns    = [ 11, 12, 15 ]
	args  = { 'atol': 1e-9, 'rtol': 1e-9 }
	cr3bp = CR3BP( 'earth-moon' )
	for n in range( 3 ):
		cr3bp.propagate_orbit( states[ n ], tspans[ n ], args )
		cr3bp.plot_2d( { 'title': f'Earth-Moon { ns[ n ] }' } )

	cr3bp = CR3BP( 'sun-jupiter' )
	cr3bp.propagate_orbit(
		[ -1.09137, 0, 0, 0, 0.14301959822238380020, 0 ],
		0.82949461922342093092e2, args )
	cr3bp.plot_2d( { 'title': 'Sun-Jupiter 19' } )
