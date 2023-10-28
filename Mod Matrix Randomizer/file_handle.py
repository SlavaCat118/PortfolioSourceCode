import json
import zipfile
import os

def open_json(path):
	f = open(path, "r")
	file = json.loads(f.read())
	f.close()
	return file

def convert_json(dict):
	return json.dumps(dict)

def first_dir(dir):
	files = os.listdir(dir)
	return files[0]

def open_bank(path, dir):
	with zipfile.ZipFile(path, 'r') as zip_path:
		zip_path.extractall(dir)

def list_dir(dir):
	files = os.listdir(dir)
	return files

def get_nested(d):
  for v in d.values():
    if isinstance(v, dict):
      yield from get_nested(v)
    else:
      yield v

def flatten_list(list):
	flat_list = [item for sublist in list for item in sublist]
	return flat_list

def create_file(path, data):
	f = open(path, "w")
	f.write(data)
	f.close()

def check_exists(path):
	if os.path.exists(path):
		return True
	else:
		return False
