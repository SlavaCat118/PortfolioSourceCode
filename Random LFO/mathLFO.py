import random
import decimal
 
#!!!CHANGE THESE THINGS!!!
author = "SlavaCat"
name = "Epic Random LFO :O"
points = 10
 
#!!!DONT CHANGE THESE!!!
LFO_points = []
powers = []
w = points-1
for y in range(points):
    z = y
    LFO_points.append(z/w)
    LFO_points.append(float(decimal.Decimal(random.randrange(0, 100))/100))
 
for y in range(w):
    powers.append(0.0)
 
LFO_points = str(LFO_points)
powers = str(powers)
help_me = (f'"author":"{author}","name":"{name}","num_points":{w},"points":{LFO_points},"powers":{powers},"smooth":false')
help_me = '{' + help_me
help_me += '}'
print(help_me)
