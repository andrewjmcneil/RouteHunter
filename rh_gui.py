"""
UI set up for RouteHunter program

Andrew McNeil, ENAE380 Flight Software Systems
December, 2020

"""

import PySimpleGUI as sg
import time

def ui():
	#apply color theme to UI window
	sg.theme('Dark Green 5')

	#input all UI text and tools, formatted accordingly
	layout = [
			[sg.Text('Welcome to RouteHunter!', font=('Helvetica Bold', 25))],

			[sg.Text('RouteHunter is a locally hosted climbing route finder')],
			[sg.Text('Please view the README.pdf for further instruction.')],
			[sg.Text('Enter your information below:')],

			[sg.Text('City:', size=(10,1))], [sg.Input(key='city')],
			[sg.Text('State (full or abbreviated) -OR- Country (if not in USA):', size=(50,1))], [sg.Input(key='state')],

			[sg.Text('Max Radius (in miles, up to 200):', size=(30,1))], [sg.Input(key='maxDist')],
			[sg.Text('Maximum grade (in YDS, up to 5.14):', size=(30,1))], [sg.Input(key='max_grade')],

			[sg.Text(size=(40,1), key='-OUTPUT-')],

			[sg.Image(filename='templates/climber.png', key='key1', size=(300, 300))],

			[sg.Button('GO', size=(10,1), font=('Helvetica', 10)), sg.Button('Quit', size=(10,1), font=('Helvetica', 10))],

			[sg.Text('Real-time route data courtesy of MountainProject.com', font=("Helvetica",10))]
			]
	#create UI window with the above layout
	window = sg.Window('RouteHunter', layout)

	#keep window open until query is found, or user quits
	while True:
		event, values = window.read()

		if event == sg.WINDOW_CLOSED or event == 'Quit':
			break
		elif event == 'GO':
			window['-OUTPUT-'].update('Searching for routes near ' + values['city'] + ", " + values['state'] + "!")
			time.sleep(2)
			break
	#auto close the window
	window.close()



	#returns user inputs, formatted for query in routehunter.py
	us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'}

	abbrev_us_state = dict(map(reversed, us_state_abbrev.items()))

	if len(values['state']) == 2:
		values['state'] = abbrev_us_state[values['state'].upper()]

	usr_input = [values['city'],values['state'],values['maxDist'],values['max_grade']]
	return(usr_input)
	pass