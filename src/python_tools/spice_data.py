'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

SPICE data filepaths
'''

import os

'''
If you set an environment variable named AWP to be
your local path to the base of this repository, you will
be able to run all scripts from any directory that you're
currently in. If not, you must run everything from the src/
directory

Here is an example of how to set this environment variable
from the terminal (I use bash):
$ export AWP=/home/alfonso/pub/AWP/

AWP_path = os.environ.get( 'AWP' )

if AWP_path is not None:
	base_dir = AWP_path
else:
	base_dir = '..'
'''
base_dir = os.path.join(
	os.path.dirname( os.path.realpath( __file__ ) ),
	'../../data/spice' )

leapseconds_kernel = os.path.join( base_dir, 'lsk/naif0012.tls' )
de432              = os.path.join( base_dir, 'spk/de432s.bsp'   )
pck00010           = os.path.join( base_dir, 'pck/pck00010.tpc' )
