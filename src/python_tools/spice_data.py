'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

SPICE data filepaths
'''

import os

base_dir = os.path.join(
	os.path.dirname( os.path.realpath( __file__ ) ),
	os.path.join( '..', '..', 'data', 'spice' ) 
	)

leapseconds_kernel = os.path.join( base_dir, 'lsk/naif0012.tls' )
de432              = os.path.join( base_dir, 'spk/de432s.bsp'   )
pck00010           = os.path.join( base_dir, 'pck/pck00010.tpc' )
