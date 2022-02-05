'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Create CR3BP Earth-Moon pseudo-potential contour plot
'''

# AWP library
import plotting_tools as pt
from CR3BP import CR3BP_SYSTEMS

if __name__ == '__main__':
	pt.plot_pseudopotential_contours( CR3BP_SYSTEMS[ 'earth-moon' ], {
		'clabels': True,
		'show'   : True
		} 
	)
