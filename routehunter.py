"""

RouteHunter Code File

Andrew McNeil
ENAE380 - Flight Software Systems
Final Project

This is the core of RouteHunter. This Python file pulls the user inputs from rh_gui then gives user 
the formatted file containing their search results.

"""

from urllib.request import Request, urlopen
import webbrowser
import json
import pandas as pd
import os

from geopy import Nominatim
import time

#python file located in zip, contains UI and receves user inputs
import rh_gui

def start():
	"""
	start function that takes in user request and runs necessary functions for data display
	"""
	usr_input = rh_gui.ui()
	
	locator = Nominatim(user_agent='myapplication')
	location = locator.geocode(str(usr_input[0]) + " " + str(usr_input[1]))
	coords = [location.latitude, location.longitude]

	usr_data = [coords[0],coords[1],usr_input[2],usr_input[3]]

	print("INPUT: " + str(usr_input[0]) + ", " + str(usr_input[1]) +".")

	get_routes(usr_data)

def get_routes(usr_data):
	"""
	core function - takes inputs and displays the best routes for given criteria
	"""
	
	print("Calculating..........")
	time.sleep(1)

	#unload input data into corresponding variables
	lat = str(usr_data[0])
	lon = str(usr_data[1])
	maxDist = str(usr_data[2])
	#user inputted max grade
	max_grade = str(usr_data[3])
	minDif = '5.4'
	maxDif = str(usr_data[3])

	#access mountainproject.com's public API, using my assigned private key 

############################################################### REQUEST SPECIFIED DATA ###################################################################
 	
 	#store given api and user-agent headers (STATIC)
	mp_api = '200977273-f35f533cfd8f1b209a8b9b6f3f3a4c23'
	user_header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36"}
	#format api request with user data
	url_gll = 'https://www.mountainproject.com/data/get-routes-for-lat-lon?lat=' + lat + '&lon=' + lon + '&maxDistance=' + maxDist + '&minDiff=' + minDif + '&maxDiff=' + maxDif + '&key=' + mp_api

	#send request as to not be flagged as a "bot"
	req = Request(url_gll)
	#open api url
	obje = urlopen(req)
	#load structure from url into json dictionary format
	data = json.load(obje)

	count = 0
	#input list of all posible climbing grades		#these comements are indices for ~ every 10 climbing grades; here for debugging purposes
	grades = ['5.4-','5.4','5.4+',					#0,1,2
				'5.5-','5.5','5.5+',
				'5.6-','5.6','5.6+',
				'5.7-','5.7','5.7+',				#9,10,11
				'5.8-','5.8','5.8+',
				'5.9-','5.9','5.9+',
				'5.10-','5.10','5.10+',				#18,19,20
				'5.10a-','5.10a','5.10a+',
				'5.10b-','5.10b','5.10b+',
				'5.10c-','5.10c','5.10c+',
				'5.10d-','5.10d','5.10d+',			#30,31,32
				'5.11-','5.11','5.11+',
				'5.11a-','5.11a','5.11a+',
				'5.11b-','5.11b','5.11b+',			#39,40,41
				'5.11c-','5.11c','5.11c+',
				'5.11d-','5.11d','5.11d+',
				'5.12-','5.12','5.12+',				#48,49,50
				'5.12a-','5.12a','5.12a+',
				'5.12b-','5.12b','5.12b+',
				'5.12c-','5.12c','5.12c+'
				'5.12d-','5.12d','5.12d+',			#60, 61, 62
				'5.13-','5.13','5.13+',
				'5.13a-','5.13a','5.13a+',
				'5.13b-','5.13b','5.13b+',			#69, 70, 71
				'5.13c-','5.13c','5.13c+',
				'5.13d-','5.13d','5.13d+',
				'5.14-','5.14','5.14+',				#78,79,80
				'5.14a-','5.14a','5.14a+',
				'5.14b-','5.14b','5.14b+',
				'5.14c-','5.14c','5.14c+',
				'5.14d-','5.14d','5.14d+',			#91,92,93
				'5.15-','5.15','5.15+',
				'5.15a-','5.15a','5.15a+',
				'5.15b-','5.15b','5.15b+',			#100, 101, 102
				'5.15c-','5.15c','5.15c+',
				'5.15d-','5.15d','5.15d+'
				]

##################################################################### FIND ROUTES ##########################################################################


	#find index of max grade, since climbing grade scale is not perfectly incremented by integer values (see all possible grades above)
	for i in range(len(grades)):
		if grades[i] == max_grade:
			grade_lim_idx = int(i)
		else:
			grade_lim_idx = int(len(grades))

	#find all routes easier than or equal to user's max grade
	found_routes = []

	for i in data["routes"]:
		if any(i['rating'] == grade for grade in grades[0:grade_lim_idx]):
			found_routes += [i['location'], i['name'] , i['rating'], i['stars']]

############################################################## FORMAT AND DISPLAY RESULTS #################################################################

	#sort found routes into list of lists, then into pandas DataFrame for easy accessing of values
	#route data was loaded into single long list, in the order of: [[Location], Name, Grade, Stars]
	sort_routes = list(map(lambda w, x, y, z:[w,x,y,z], 
		found_routes[0:len(found_routes)-3:4],found_routes[1:len(found_routes)-3:4],
		found_routes[2:len(found_routes)-3:4],found_routes[3:len(found_routes)-1:4]))

	df_routes = pd.DataFrame(sort_routes, columns = ['Location', 'Name', 'Grade', 'Stars']) 
	#rearrange dataframe to have routes sorted by their rating 
	sorted_df = df_routes.sort_values(by = 'Stars', ascending=False).reindex(columns= ['Name','Location','Grade', 'Stars'])

	#html file skeleton, including title and header information, prepped to have rh_style.css file applied
	html_format = '''
	<!-- 
	RouteHunter Query Result

	Open me in a browser! I'm HTML!

	Andrew McNeil; December 2020
	-->
	<html>
  		<head><title>Route Hunter</title></head>
  		<link rel="stylesheet" type="text/css" href="rh_style.css"/>
  		<body>
    		{table}
  		</body>
	</html>
				'''
	#convert the dataframe to html, write it over the pre-downloaded routes_df.html file in the routehunter dir.
	html_df = sorted_df.to_html(classes='style',justify="left",na_rep = "", index = False).replace('<th>','<th style = "background-color: #194d30; color: #ffffff">')
	routes_file = open("templates/routes_df.html","w+")
	routes_file.write(html_format.format(table=html_df))
	routes_file.close()

	#auto-launch the .html file in user's default browser
	print("Opening your routes....")
	time.sleep(1)
	print("Done!")
	routes_file = 'file:///'+os.getcwd()+'/' + 'templates/routes_df.html'
	webbrowser.open_new_tab(routes_file)


######################################################################## MAIN #################################################################################
 
if __name__ == '__main__':
    start()

