import json
import os

def convert(dict_):
	return [
		dict_["operator"],
		[convert(i) for i in dict_["args"]]
	]

valid = [i for i in os.listdir() if ".JSON" in i]
for file in valid:
	converted = None
	with open(file,"r") as f:
		data = json.load(f)
		converted = convert(data)
	with open(file,"w") as f:
		f.write(json.dumps(converted))
