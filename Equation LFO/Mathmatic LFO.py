import numpy
import math as m

#!!! CHANGE THESE !!!----------------------------------------------------------
AUTHOR = 'the guy'
NAME = 'MATH LFO >:O'
X_RANGE = [1,2] #DISTANCE BETWEEN * RESOLUTION MUST BE <= 100 ALSO NO DECIMALS
#Number of subdivisions between points | 1 = none                              
RESOLUTION = 30
#How many decimals to round to
ROUND_RANGE = 3

def equation(x_pos):
	#!!! ADD VARIABLES HERE X IS DEFAULT !!!                                  
	x = x_pos
	#!!! INSTER EQUATION HERE | ADD 'm.' BEFORE OPPERATION !!!           
	y = m.tan(m.sin(m.cos(m.sin(m.tan(x)/1)/1)))
	#!!! OK STOP CHANGING THINGS >:( !!!                                    
	return y
#------------------------------------------------------------------------------

VITAL_RANGE = [0,1]

def scale_toRange(unscaled,range_start,range_end):
	scaled = numpy.ndarray.tolist(numpy.interp(unscaled, (min(unscaled), max(unscaled)), (range_start,range_end)))
	return scaled

def round_list(unrounded,round_amount):
	for x in range(len(unrounded)):
		unrounded[x] = round(unrounded[x],ROUND_RANGE)
	return unrounded

#Set points
POINTS = (abs(X_RANGE[0]-X_RANGE[1])*RESOLUTION)
powers = []
for n in range(POINTS):
	powers.append(0)
if POINTS >= 200:
	print("!!!WARNING!!! THIS MANY POINTS COULD CRASH VITAL !!!WARNING!!!\n")

#Creating the x_values
x_values = []
for x in range((X_RANGE[0]*RESOLUTION),(X_RANGE[1]*RESOLUTION)):
	x_values.append(x)

#Scaling the values back to range
x_values = scale_toRange(x_values,X_RANGE[0],X_RANGE[1])

#Creating y_values from equation
y_values = []
for x_pos in range(POINTS):
	x = x_values[x_pos]
	y_values.append(equation(x))

#Scaling x to the Vital range of (0,1)
x_values = scale_toRange(x_values,VITAL_RANGE[0],VITAL_RANGE[1])
x_values = round_list(x_values,ROUND_RANGE)

#Again scaling y to Vital range
y_values = scale_toRange(y_values,VITAL_RANGE[0],VITAL_RANGE[1])
y_values = round_list(y_values,ROUND_RANGE)

#Combine
LFO_points = []
for x in range(POINTS):
	LFO_points.extend((x_values[x],y_values[x]))
paste = '{' + (f'"author":"{AUTHOR}","name":"{NAME}","num_points":{POINTS},"points":{LFO_points},"powers":{powers},"smooth":false') + '}'
print(paste)
print('\n')
if POINTS > 100:
	print('You have too many points, results might not be as expected :/')

# {"author": "SlavaCat", "name": "EquaFO LFO", "num_points": 30, "points": [0.0, 0.035, 0.069, 0.104, 0.138, 0.172, 0.207, 0.241, 0.276, 0.31, 0.345, 0.379, 0.414, 0.448, 0.483, 0.517, 0.552, 0.586, 0.621, 0.655, 0.69, 0.724, 0.759, 0.793, 0.828, 0.862, 0.896, 0.931, 0.965, 1.0, 0.501], "powers": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "smooth": True}
# {"author":"the guy","name":"MATH LFO >:O","num_points":30,"points":[0.0, 0.0, 0.034, 0.011, 0.069, 0.054, 0.103, 0.141, 0.138, 0.283, 0.172, 0.488, 0.207, 0.736, 0.241, 0.95, 0.276, 0.977, 0.31, 0.645, 0.345, 0.11, 0.379, 0.165, 0.414, 1.0, 0.448, 0.06, 0.483, 0.094, 0.517, 0.96, 0.552, 0.28, 0.586, 0.192, 0.621, 0.13, 0.655, 0.511, 0.69, 0.221, 0.724, 0.963, 0.759, 0.245, 0.793, 0.07, 0.828, 0.588, 0.862, 0.96, 0.897, 0.966, 0.931, 0.762, 0.966, 0.513, 1.0, 0.302],"powers":[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],"smooth":false}