'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

World cities dictionaries for groundtracks plots
'''

# standard Python libraries
import os

WORLD_CITIES_FILE = os.path.join(
	os.path.dirname( os.path.realpath( __file__ ) ),
	os.path.join( '..', '..', 'data', 'earth_data', 'world_cities.csv' )
	)

city_list0 = [
	 'Seattle', 'Pasadena',                 # US
	 'New York', 'San Luis Obispo',
	 'Phoenix', 'Cape Canaveral',
	 'Mexico City', 'Villahermosa',         # Mexico
	 'New Delhi', 'Mumbai',                 # India
	 'Tirunelveli', 'Surat', 'Chennai',
	 'Olney', 'Norwich',                    # England
	 'Ponce',                               # Puerto Rico
	 'Berlin',                              # Germany
	 'Lyon',                                # France
	 'Vienna',                              # Austria
	 'Madrid', 'Sevilla', 'Barcelona',      # Spain
	 'Moscow',                              # Russia
	 'Rome', 'Cortemaggiore',               # Italy
	 'Aalborg',                             # Denmark
	 'Sao Paulo',                           # Brazil
	 'Luxembourg City', 'Esch-sur-Alzette', # Luxembourg
	 'Toronto',                             # Canada
	 'Tokyo',                               # Japan
	 'Istanbul',                            # Turkey
	 'Jihlava',                             # Czech Republic
	 'Warsaw',                              # Poland
	 'Zagreb',                              # Croatia
	 'Sydney', 'Adelaide',                  # Australia
	 'Dubai',                               # UAE
	 'Port Louis',                          # Mauritius
	 'Casablanca',                          # Morocco
	 'Khartoum',                            # Sudan
	 'Tunis',                               # Tunisia
	 'Buenos Aires',                        # Argentina
	 'Cape Town',                           # South Africa
	 'Bucharest',                           # Romania
	 'Bogota',                              # Colombia
	 'Quito',                               # Ecuador
	 'Noordwijk',                           # Netherlands
	 'San Jose',                            # Costa Rica
	 'Stockholm',                           # Sweden
	 'Santiago',                            # Chile
	 'Jakarta',                             # Indonesia
	 'Antwerp',                             # Belgium
	 'Geneva',                              # Switzerland
	 'Manila',                              # Phillipines
	 'Porto', 'Ponta Delgada',              # Portugal
	 'Budapest',                            # Hungary
	 'Panama City',                         # Panama
	 'Cairo',                               # Egypt
	 'Seoul',                               # South Korea
	 'Broom Bridge',                        # Ireland
	 'Lima',                                # Peru
	 'Akure'                                # Nigeria
]

def city_dict():
	with open( WORLD_CITIES_FILE, 'r' ) as f:
		lines = f.readlines()

	header = lines[ 0 ]
	cities = {}

	for line in lines[ 1: ]:
		line = line.split(',')

		# create new dictionary for given city
		try:
			# city name and lat/long coordinates
			cities[ line[ 1 ] ] = [ float( line[ 2 ] ), float( line[ 3 ] ) ]

		except:
			pass

	return cities