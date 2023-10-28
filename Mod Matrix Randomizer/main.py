import file_handle as fh
import decimal
import random
from tkinter import *

create_files = 1
random_preset_type = 1
# Import Data, sources, destinations, usable, default.vital
def import_data():
	imports, data = ['sources.json', 'destinations.json', 'usable.json','default.vital', 's_groups.json','d_groups.json'], []
	for path in imports:
		data.append(fh.open_json(f"data/{path}"))
	return data

# Get a list of presets
def get_preset_list(dir):
	paths = fh.list_dir(dir)
	return paths

def open_preset(path, dir):
	if dir != '':
		patch = fh.open_json(f"{dir}/{path}")
	else:
		patch = fh.open_json(path)
	return patch

def randomize_matrix(matrix, sources, destinations, modulations, restrictions):
	x, dest = 0, []
	for z in range(int(modulations)):
		mods = matrix[z]
		if restrictions != 'Restrict to Macros':
			mods['source'] = sources[random.randrange(len(sources))]
		else:
			mods['source'] = sources[random.randrange(14,17)]
		y = random.randrange(len(destinations))
		mods['destination'] = destinations[y]
		dest.append(y)
		matrix[x] = {'source':mods['source'],'destination':mods['destination']}
		x += 1
		data = [matrix, dest]
	return data

def enable_used(matrix, patch, usable):
	#get a list of used destinations
	destinations = []
	for x in matrix:
		for key,value in x.items():
			destinations.append(value)
	enable = []
	for x in destinations:
		for yes in usable:
			if yes in x:
				enable.append(yes)
	for x in enable:
		patch['settings'][f'{x}on'] = 1.0
	return patch

def randomize_amount(patch):
	for x in range(64):
		x += 1
		patch['settings'][f'modulation_{x}_amount'] = float(decimal.Decimal(random.randrange(-100, 100))/100)
		patch['settings'][f'modulation_{x}_bipolar'] = float(decimal.Decimal(random.randrange(-1,1)))
		patch['settings'][f'modulation_{x}_power'] = float(decimal.Decimal(random.randrange(-100, 100))/10)
		patch['settings'][f'modulation_{x}_stereo'] = float(decimal.Decimal(random.randrange(-1,1)))
	return patch

def create_preset(path, preset_dir, un_sources, un_destinations, usable, settings):
	patch = open_preset(path, preset_dir)
	data = randomize_matrix(patch['settings']['modulations'], un_sources, un_destinations, settings[1], settings[2])
	patch['settings']['modulations'] = data[0]
	used = data[1]
	patch = enable_used(patch['settings']['modulations'], patch, usable)
	patch = randomize_amount(patch)
	return patch

def gui():
	cr = 0
	def info():
		info_window = Tk()
		info_window.title("How To Use")
		def exit():
			info_window.destroy()
		Label (info_window, text = 'To start, put your base preset (the preset that will get a randomized matrix) in the "presets_here" folder\nYou can put as many presets here as you like, but it is recommended to only do 1 or 2 to make everything go fast\nNext just fill out all the settings in the main window.\nAfter your press "Generate", all the new presets can be found in the "final_presets" folder.\nIf you have any trouble, just contact me on the Vital Forums: https://forum.vital.audio/u/slavacat/').grid(row = 0, column = 0, sticky = W)
		Button(info_window, text = 'Exit', command = exit).grid(row = 1, column = 0, sticky = S)
		info_window.mainloop()
	def get_vars():
		setting_list[0] = create_amount.get()
		if int(setting_list[0]) > 10:
			setting_list[0] = '10'
		setting_list[1] = modulation_amount.get()
		setting_list[2] = source_res.get()
		window.destroy()
	#colors
	bg, text, fg, font = 'grey5','MediumPurple1','thistle1','Segoe UI Light'
	#configure
	window = Tk()
	window.title("Mod Matrix Randomizer")
	window.configure(bg = bg)
	setting_list = ['','',''] #New preset amount; Amount of modulations: 0-64; Source type: 0 = all sources, 1 = limit to macros; 
	#images
	icon = PhotoImage(file = 'icon.gif')
	logo = PhotoImage(file = 'vital_tools.gif')
	#displays
	window.iconphoto(False, icon)
	Button(window, text = 'How to Use?', command = info).grid(row = cr, column = 0, sticky = W)
	cr += 1
	Label (window, image = logo, bg = bg).grid(row = cr, column = 0, sticky = S)
	cr += 1
	Label (window, text = 'By: Vital Tools/SlavaCat', bg = bg, fg = text, font = (font, 11)).grid(row = cr, column = 0, sticky = S)
	cr += 1
	Label (window, text = 'Welcome to Mod Matrix Randomizer for Vital!', bg = bg, fg = text, font = (font, 18)).grid(row = cr, column = 0, sticky = S)
	cr += 1
	Label (window, text = 'Enter in the amount of new presets you want: \nWARNING: THIS WILL MULTIPLY WITH THE AMOUNT OF PRESETS YOU HAVE IN THE PRESET FOLDER',bg = bg, fg = text, font = (font, 11)).grid(row = cr, column = 0, sticky = S)
	cr += 1
	create_amount = Entry(window, width = 10, bg = fg)
	create_amount.grid(row = cr, column = 0, sticky = S)
	cr += 1
	Label (window, text = 'Enter in the amount modulations you want: (1-64)',bg = bg, fg = text, font = (font, 11)).grid(row = cr, column = 0, sticky = S)
	cr += 1
	modulation_amount = Entry(window, width = 10, bg = fg)
	modulation_amount.grid(row = cr, column = 0, sticky = S)
	cr += 1
	Label (window, text = 'Source restrictions?',bg = bg, fg = text, font = (font, 11)).grid(row = cr, column = 0, sticky = S)
	cr += 1
	source_res = StringVar()
	OptionMenu(window, source_res, 'No source restrictions','Restrict to Macros').grid(row = cr, column = 0, sticky = S)
	cr += 1
	Button(window, text = 'Generate', command = get_vars).grid(row = cr, column = 0, sticky = S)
	# Getting Info

	window.mainloop()
	return setting_list

def main():
	# Get Data
	data = import_data()
	sources, destinations, usable, default, s_groups, d_groups = data[0], data[1], data[2], data[3], data[4], data[5]
	# Unnest them
	un_sources = fh.flatten_list(list(fh.get_nested(sources)))
	un_destinations = fh.flatten_list(list(fh.get_nested(destinations)))
	preset_dir = 'presets_here'
	#gui
	setting_list = gui()
	# Get paths in preset dir
	paths = get_preset_list(preset_dir)
	x = 0
	presets = []
	create_files = int(setting_list[0])
	for x in range(create_files):
		for path in paths:
			patch = create_preset(path, preset_dir, un_sources, un_destinations, usable, setting_list)
			presets.append(patch)
			fh.create_file(f'final_presets/{x}{path}', fh.convert_json(patch))
			x += 1

main()