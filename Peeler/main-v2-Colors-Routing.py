import colorzero as cz
import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
from tkinter import simpledialog
import json
import os

r = tk.Tk()
r.geometry("+10+10")
root = ttk.Frame(r)
root.grid(row = 0, column = 0, sticky = tk.NSEW, padx = 5, pady = 10)

def readJson(path):
	with open(path, 'r') as f:
		return json.load(f)

def writeJson(path, text):
	with open(path, 'w+') as f:
		f.write(json.dumps(text, indent = 4))

####################################################################### Color Maker

# Color/Value maker values are stored separately from file maker values but can be stored together in a .peeler file

	### Vars ###

labelConnections = {} # {prefabId:"LabelName"}

colorList  = {} # iD:{iD, name, color}
filterList = {} # iD:{iD, name, h, s, l}
prefabList = {} # iD:{iD, name, path:{filters, color}}

colorTemplateList = []
colorTemplateSel = tk.StringVar()

	### Objects ###

colorMaker = ttk.Frame(root)

s = ttk.Style()

	### Formatting ###

colorMaker.grid(row = 0, column = 0, sticky = tk.NSEW)

s.configure('labelTree.Treeview', rowheight=41)
s.configure('folderTree.Treeview', rowheight=41)

#################################################################### Color Frame

	### Functions ###

def toggleItem(item, r, c, button, text):
	if item.winfo_ismapped():
		item.grid_forget()
		button.config(text = text[0])
	else:
		item.grid(row = r, column = c, sticky = tk.N, padx = 5)
		button.config(text = text[1])

	### Objects ###

colorFrame        = ttk.Frame(colorMaker)
colorHeader       = ttk.Frame(colorMaker)
colorFrameButtons = ttk.Frame(colorHeader)

colorCollapse  = ttk.Button(colorFrameButtons, text = "C", command = lambda:toggleItem(colorFrame, 2, 0, colorCollapse, ("c","C")), width = 3)
filterCollapse = ttk.Button(colorFrameButtons, text = "F", command = lambda:toggleItem(filterFrame, 2, 1, filterCollapse, ("f","F")), width = 3)
prefabCollapse = ttk.Button(colorFrameButtons, text = "P", command = lambda:toggleItem(prefabFrame, 2, 2, prefabCollapse, ("p","P")), width = 3)
labelCollapse  = ttk.Button(colorFrameButtons, text = "L", command = lambda:toggleItem(labelFrame, 2, 0, labelCollapse, ("l","L")), width = 3)
modCollapse    = ttk.Button(colorFrameButtons, text = "M", command = lambda:toggleItem(modFrame, 2, 1, modCollapse, ("m","M")), width = 3)
destCollapse   = ttk.Button(colorFrameButtons, text = "D", command = lambda:toggleItem(destFrame, 2, 2, destCollapse, ("d","D")), width = 3)

	### Formatting ###

colorHeader            .grid(row = 0, column = 0, sticky = tk.NSEW, columnspan = 3)
colorFrame             .grid(row = 2, column = 0, sticky = tk.NSEW, padx = 5)

colorFrameButtons      .grid(row = 0, column = 0, sticky = tk.W)
colorCollapse          .grid(row = 0, column = 0, sticky = tk.NSEW)
filterCollapse         .grid(row = 0, column = 1, sticky = tk.NSEW)
prefabCollapse         .grid(row = 0, column = 2, sticky = tk.NSEW)
labelCollapse          .grid(row = 0, column = 3, sticky = tk.NSEW)
modCollapse            .grid(row = 0, column = 4, sticky = tk.NSEW)
destCollapse           .grid(row = 0, column = 5, sticky = tk.NSEW)

################################################################# Color Presets

	### Vars ###

colorPresetList = []
colorPresetSel = tk.StringVar()

	### Functions ###

def getColorPresets():
	for i in os.listdir("userData/color"):
		colorPresetList.append(i.split(".")[0])

def addColorPreset(path):
	if os.path.exists(path):
		preset = readJson(path)
		for i in preset:
			toAdd = preset[i]
			toAdd['iD'] = getNextColorId()
			addColor(toAdd)

def createColorPreset(iDs):
	if len(iDs) > 0:
		preset = {}
		for i in iDs:
			preset[i] = colorList[i]
		pathName = simpledialog.askstring("Name", "Preset Name: ")
		if pathName != None:
			writeJson("userData/color/" + pathName + ".json", preset)

getColorPresets()

	### Objects ###

colorPresetFrame = ttk.Frame(colorFrame)

colorPresetMenu = ttk.OptionMenu(colorPresetFrame, colorPresetSel, "Color Presets", *colorPresetList)

colorPresetAddButton  = ttk.Button(colorPresetFrame, text = "Add", width = 5, command = lambda:addColorPreset(os.path.join("userData/color",colorPresetSel.get() + ".json")))
colorPresetSaveButton = ttk.Button(colorPresetFrame, text = "Save Selected", command = lambda:createColorPreset(colorTree.selection()))

	### Formatting ###

colorPresetMenu.config(width = 12)

colorPresetFrame     .grid(row = 0, column = 0, sticky = tk.NSEW)
colorPresetMenu      .grid(row = 0, column = 0, sticky = tk.NSEW)
colorPresetAddButton .grid(row = 0, column = 1, sticky = tk.NSEW)
colorPresetSaveButton.grid(row = 0, column = 2, sticky = tk.NSEW)

################################################################# Color Tree

	### Functions ###

def getNextColorId():
	iD = 0
	while str(iD) in colorList.keys():
		iD += 1
	return str(iD)

def selectedColor():
	return None if colorTree.focus() == '' else colorTree.focus()

def updateColorTree():
	for i in colorList:
		colorTree.tag_configure(i, background = colorList[i]['color'])

def replaceColor(iD, newVal):
	if newVal != None and iD != None:
		newVal['iD'] = iD
		colorTree.item(iD, text = iD + " : " + newVal['name'])
		colorList[iD] = newVal
		updateColorTree()
		updateFilterTree()
		updatePrefabTree()
		updateFilterBox()
		updatePrefabBox()

def removeColor(iDs):
	for i in iDs:
		colorTree.delete(i)
		colorList.pop(i)

def addColor(newVal):
	if newVal != None and newVal['iD'] != "":
		colorTree.insert(parent = "", index = 'end', id = newVal['iD'], text = newVal['iD'] + " : " + newVal['name'], tags = [newVal['iD']])
		colorTree.tag_configure(newVal['iD'], background = newVal['color'])
		colorList[newVal['iD']] = newVal

	### Objects ###

colorTree = ttk.Treeview(colorFrame)

	### Formatting ###

colorTree.grid(row = 1, column = 0, sticky = tk.NSEW)

colorTree.heading("#0", text = "Colors")
colorTree.column("#0", width = 200)

	### Misc ###

colorTree.bind("<Double-1>", lambda x:setColorBox(colorList[selectedColor()]))

################################################################# Color Box

	### Vars ###

colorNameVar = tk.StringVar()
colorIdVar   = tk.StringVar()
colorValVar  = tk.StringVar()

rVar = tk.IntVar()
gVar = tk.IntVar()
bVar = tk.IntVar()

colorIdVar.set(0)

rVar.set(1)
gVar.set(4)
bVar.set(9)

	### Functions ###

def updateColorBox(copy = False):
	currentColor = str(cz.Color(rVar.get(), gVar.get(), bVar.get()))
	colorValVar.set(currentColor)
	colorView.configure(bg = currentColor)
	if copy:
		r.clipboard_clear()  # clear clipboard contents
		r.clipboard_append(currentColor)

def getColorBox():
	if colorIdVar.get() in colorList.keys():
		colorIdVar.set(getNextColorId())
	return {"iD": colorIdVar.get(), "name": colorNameVar.get(), "color": getColor()}

def getColor():
	updateColorBox()
	return colorValVar.get().strip()

def setColorBox(newVal):
	if newVal != None:
		colorIdVar.set(newVal['iD'])
		colorNameVar.set(newVal['name'])
		colorValVar.set(newVal['color'])
		c = cz.Color(newVal['color']).rgb_bytes
		rVar.set(c[0])
		gVar.set(c[1])
		bVar.set(c[2])
		updateColorBox()

def browseColor():
	try:
		newColor = colorchooser.askcolor(color = colorValVar.get())
	except Exception:
		newColor = colorchooser.askcolor()
	if newColor[0] != None:
		colorValVar.set(newColor[1])
		c = cz.Color(newColor[1]).rgb_bytes
		rVar.set(c[0])
		gVar.set(c[1])
		bVar.set(c[2])
		updateColorBox()

def roundColorBoxSliders(*args):
	rVar.set(round(rVar.get()))
	gVar.set(round(gVar.get()))
	bVar.set(round(bVar.get()))
	updateColorBox()

	### Objects ###

colorBox = ttk.Frame(colorFrame)

colorSliders = ttk.LabelFrame(colorBox, text = "Sliders")
colorInfo    = ttk.LabelFrame(colorBox, text = "ID : Name")

colorView   = tk.Button(colorBox, relief = "sunken", command = lambda:updateColorBox(copy = True))
colorBrowse = ttk.Button(colorBox, text = "Browse", width = 8, command = browseColor)

colorLabelR    = ttk.Label(colorSliders, text = "R")
colorLabelG    = ttk.Label(colorSliders, text = "G")
colorLabelB    = ttk.Label(colorSliders, text = "B")
colorSeparator = ttk.Label(colorInfo, text = " : ", width = 1)

colorSliderR = ttk.Scale(colorSliders, from_ = 255, to = 0, var = rVar, orient = "vertical", command = roundColorBoxSliders)
colorSliderG = ttk.Scale(colorSliders, from_ = 255, to = 0, var = gVar, orient = "vertical", command = roundColorBoxSliders)
colorSliderB = ttk.Scale(colorSliders, from_ = 255, to = 0, var = bVar, orient = "vertical", command = roundColorBoxSliders)

colorRead   = ttk.Entry(colorBox, textvariable = colorValVar, width = 10)
colorId     = ttk.Spinbox(colorInfo, textvariable = colorIdVar, width = 5, from_ = 0, to = 100, increment = 1, wrap = False)
colorName   = ttk.Entry(colorInfo, textvariable = colorNameVar, width = 15)
colorBoxAdd = ttk.Button(colorInfo, text = "Add", command = lambda : addColor(getColorBox()), width = 10)
colorEntryR = ttk.Entry(colorSliders, textvariable = rVar, width = 4)
colorEntryG = ttk.Entry(colorSliders, textvariable = gVar, width = 4)
colorEntryB = ttk.Entry(colorSliders, textvariable = bVar, width = 4)

colorBoxAdd.bind("<Return>", lambda x: addColor(getColorBox()))

	### Formatting ###

colorBox      .grid(row = 3, column = 0, sticky = tk.NSEW)
colorView     .grid(row = 0, column = 0, sticky = tk.NSEW, columnspan = 2, ipady = 50, ipadx = 61)
colorRead     .grid(row = 1, column = 0, sticky = tk.NSEW)
colorBrowse   .grid(row = 1, column = 1, sticky = tk.NSEW)

colorInfo     .grid(row = 2, column = 0, sticky = tk.NSEW, columnspan = 3)
colorId       .grid(row = 0, column = 0, sticky = tk.NSEW)
colorSeparator.grid(row = 0, column = 1, sticky = tk.NSEW)
colorName     .grid(row = 0, column = 2, sticky = tk.NSEW)
colorBoxAdd   .grid(row = 0, column = 3, sticky = tk.NSEW)

colorSliders  .grid(row = 0, column = 2, sticky = tk.NSEW, rowspan = 2)
colorLabelR   .grid(row = 0, column = 0, sticky = tk.NSEW)
colorLabelG   .grid(row = 0, column = 1, sticky = tk.NSEW)
colorLabelB   .grid(row = 0, column = 2, sticky = tk.NSEW)
colorSliderR  .grid(row = 1, column = 0, sticky = tk.NSEW)
colorSliderG  .grid(row = 1, column = 1, sticky = tk.NSEW)
colorSliderB  .grid(row = 1, column = 2, sticky = tk.NSEW)
colorEntryR   .grid(row = 2, column = 0, sticky = tk.NSEW)
colorEntryG   .grid(row = 2, column = 1, sticky = tk.NSEW)
colorEntryB   .grid(row = 2, column = 2, sticky = tk.NSEW)

################################################################# Color Buttons

	### Objects ###

colorButtons = ttk.Frame(colorFrame)

replaceColorButton = ttk.Button(colorButtons, text = "Replace", command = lambda : replaceColor(selectedColor(), getColorBox()))
removeColorButton  = ttk.Button(colorButtons, text = "Remove" , command = lambda : removeColor(colorTree.selection()))
addColorButton     = ttk.Button(colorButtons, text = "Add"    , command = lambda : addColor(getColorBox()))

	### Formatting

colorButtons      .grid(row = 2, column = 0, sticky = tk.NSEW, pady = (10, 0))
replaceColorButton.grid(row = 0, column = 0, sticky = tk.NSEW)
removeColorButton .grid(row = 0, column = 1, sticky = tk.NSEW)
addColorButton    .grid(row = 0, column = 2, sticky = tk.NSEW)

#################################################################### Filter Frame

	### Objects ###

filterFrame = ttk.Frame(colorMaker)

	### Formatting ###

filterFrame.grid(row = 2, column = 1, sticky = tk.NSEW, padx = 5)

################################################################# Filter Presets

	### Vars ###

filterPresetList = []
filterPresetSel = tk.StringVar()

	### Functions ###

def getFilterPresets():
	for i in os.listdir("userData/filter"):
		filterPresetList.append(i.split(".")[0])

def addFilterPreset(path):
	if os.path.exists(path):
		preset = readJson(path)
		for i in preset:
			toAdd = preset[i]
			toAdd['iD'] = getNextFilterId()
			addFilter(toAdd)

def createFilterPreset(iDs):
	if len(iDs) > 0:
		preset = {}
		for i in iDs:
			preset[i] = filterList[i]
		pathName = simpledialog.askstring("Name", "Preset Name: ")
		if pathName != None:
			writeJson("userData/filter/" + pathName + ".json", preset)

getFilterPresets()

	### Objects ###

filterPresetFrame = ttk.Frame(filterFrame)

filterPresetMenu = ttk.OptionMenu(filterPresetFrame, filterPresetSel, "Filter Presets", *filterPresetList)

filterPresetAddButton  = ttk.Button(filterPresetFrame, text = "Add", width = 5, command = lambda:addFilterPreset(os.path.join("userData/filter",filterPresetSel.get() + ".json")))
filterPresetSaveButton = ttk.Button(filterPresetFrame, text = "Save Selected", command = lambda:createFilterPreset(filterTree.selection()))

	### Formatting ###

filterPresetMenu.config(width = 12)

filterPresetFrame     .grid(row = 0, column = 0, sticky = tk.NSEW)
filterPresetMenu      .grid(row = 0, column = 0, sticky = tk.NSEW)
filterPresetAddButton .grid(row = 0, column = 1, sticky = tk.NSEW)
filterPresetSaveButton.grid(row = 0, column = 2, sticky = tk.NSEW)

################################################################# Filter Tree

	### Functions ###

def selectedFilter():
	return None if filterTree.focus() == '' else filterTree.focus()

def updateFilterTree(*args):
	if selectedColor() != None:
		for i in filterTree.get_children():
			filterTree.tag_configure(i, background = applyFilter(filterList[i], colorList[selectedColor()]['color']))

def getNextFilterId():
	iD = 0
	while str(iD) in filterList.keys():
		iD += 1
	return str(iD)

	### Objects ###

filterTree = ttk.Treeview(filterFrame)

	### Formatting ###

filterTree.grid(row = 1, column = 0, sticky = tk.NSEW)

filterTree.heading("#0", text = "Filters")
filterTree.column("#0", width = 190)

filterTree.bind("<Double-1>", lambda x:setFilterBox(filterList[filterTree.focus()]))

################################################################# Filter Box

	### Vars ###

filterNameVar    = tk.StringVar()
filterIdVar      = tk.StringVar()

filterIdVar.set(0)

hVar = tk.IntVar()
sVar = tk.IntVar()
lVar = tk.IntVar()
aVar = tk.IntVar()

hVar.set(16)
sVar.set(25)
lVar.set(36)

	### Functions ###

def getFilterBox():
	if filterIdVar.get() in filterList.keys():
		filterIdVar.set(getNextFilterId())
	return {"iD":filterIdVar.get(),"name":filterNameVar.get(),"h":hVar.get(),"s":sVar.get(),"l":lVar.get(),"a":aVar.get()}

def setFilterBox(newVal):
	if newVal != None:
		filterIdVar.set(newVal['iD'])
		filterNameVar.set(newVal['name'])
		hVar.set(newVal['h'])
		sVar.set(newVal['s'])
		lVar.set(newVal['l'])
		aVar.set(newVal['a'])
		updateFilterBox()

def updateFilterBox(copy = False):
	filterColor = selectedColor()
	if filterColor != None:
		currentColor = applyFilter(getFilterBox(), colorList[filterColor]['color'])
		filterView.configure(background = currentColor)
		if copy:
			r.clipboard_clear()
			r.clipboard_append(currentColor)

def roundFilterBoxSliders(*args):
	hVar.set(round(hVar.get()))
	sVar.set(round(sVar.get()))
	lVar.set(round(lVar.get()))
	aVar.set(round(aVar.get()))
	updateFilterBox()

def applyFilter(filter, color):
	if color != None:
		c = cz.Color(color)
		c = c + cz.Hue(filter['h']*(1/255))
		c = c + cz.Saturation(filter['s']*(1/255))
		c = c + cz.Lightness(filter['l']*(1/255))
		return str(c)
	return "#FFFFFF"

	### Objects ###

filterBox = ttk.Frame(filterFrame)

filterSliders = ttk.LabelFrame(filterBox, text = "Sliders")
filterInfo = ttk.LabelFrame(filterBox, text = "ID : Name")

filterView = tk.Button(filterBox, relief = "sunken", command = lambda:updateFilterBox(copy = True))

filterLabelH    = ttk.Label(filterSliders, text = "H")
filterLabelS    = ttk.Label(filterSliders, text = "S")
filterLabelL    = ttk.Label(filterSliders, text = "L")
filterLabelA    = ttk.Label(filterSliders, text = "A")
filterSeparator = ttk.Label(filterInfo, text = " : ", width = 1)

filterSliderH = ttk.Scale(filterSliders, from_ = 255, to = -255, var = hVar, orient = "vertical", command = roundFilterBoxSliders)
filterSliderS = ttk.Scale(filterSliders, from_ = 255, to = -255, var = sVar, orient = "vertical", command = roundFilterBoxSliders)
filterSliderL = ttk.Scale(filterSliders, from_ = 255, to = -255, var = lVar, orient = "vertical", command = roundFilterBoxSliders)
filterSliderA = ttk.Scale(filterSliders, from_ = 255, to = -255, var = aVar, orient = "vertical", command = roundFilterBoxSliders)

filterEntryH = ttk.Entry(filterSliders, textvariable = hVar, width = 4)
filterEntryS = ttk.Entry(filterSliders, textvariable = sVar, width = 4)
filterEntryL = ttk.Entry(filterSliders, textvariable = lVar, width = 4)
filterEntryA = ttk.Entry(filterSliders, textvariable = aVar, width = 4)
filterId     = ttk.Spinbox(filterInfo, textvariable = filterIdVar, width = 5, from_ = 0, to = 100, increment = 1, wrap = False)
filterName   = ttk.Entry(filterInfo, textvariable = filterNameVar, width = 15)
filterBoxAdd = ttk.Button(filterInfo, text = "Add", command = lambda:addFilter(getFilterBox()), width = 10)

	### Formatting ###

filterBox      .grid(row = 3, column = 0, sticky = tk.NSEW)
filterView     .grid(row = 0, column = 0, sticky = tk.NSEW, columnspan = 2, ipady = 65, ipadx = 46)

filterInfo     .grid(row = 1, column = 0, sticky = tk.NSEW, columnspan = 3)
filterId       .grid(row = 0, column = 0, sticky = tk.NSEW)
filterSeparator.grid(row = 0, column = 1, sticky = tk.NSEW)
filterName     .grid(row = 0, column = 2, sticky = tk.NSEW)
filterBoxAdd   .grid(row = 0, column = 3, sticky = tk.NSEW)

filterSliders  .grid(row = 0, column = 2, sticky = tk.NSEW)
filterLabelH   .grid(row = 0, column = 0, sticky = tk.NSEW)
filterLabelS   .grid(row = 0, column = 1, sticky = tk.NSEW)
filterLabelL   .grid(row = 0, column = 2, sticky = tk.NSEW)
filterSliderH  .grid(row = 1, column = 0, sticky = tk.NSEW)
filterSliderS  .grid(row = 1, column = 1, sticky = tk.NSEW)
filterSliderL  .grid(row = 1, column = 2, sticky = tk.NSEW)
filterEntryH   .grid(row = 2, column = 0, sticky = tk.NSEW)
filterEntryS   .grid(row = 2, column = 1, sticky = tk.NSEW)
filterEntryL   .grid(row = 2, column = 2, sticky = tk.NSEW)
# filterLabelA   .grid(row = 0, column = 3, sticky = tk.NSEW)
# filterSliderA  .grid(row = 1, column = 3, sticky = tk.NSEW)
# filterEntryA   .grid(row = 2, column = 3, sticky = tk.NSEW)

	### Misc ###

colorTree.bind("<<TreeviewSelect>>", lambda x:[updateFilterBox(), updateFilterTree(), updatePrefabBox()])
filterSliderS.bind("<Double-1>", lambda x: sVar.set(0))
filterSliderH.bind("<Double-1>", lambda x: hVar.set(0))
filterSliderL.bind("<Double-1>", lambda x: lVar.set(0))

################################################################# Filter Buttons

	### Vars ###

lockFilter = tk.BooleanVar()

	### Functions ###

def replaceFilter(iD, newVal):
	if iD != None:
		newVal['iD'] = iD
		filterTree.item(iD, text = newVal['iD'] + " : " + newVal['name'])
		filterList[iD] = newVal
		if selectedColor() != None:
			filterTree.tag_configure(iD, background = applyFilter(filterList[iD], colorList[selectedColor()]['color']))
		updateFilterTree()
		updatePrefabTree()
		updatePrefabBox()

def removeFilter(iDs):
	for i in iDs:
		filterTree.delete(i)
		filterList.pop(i)

def addFilter(newVal):
	if newVal != None and newVal['iD'] != "":
		filterTree.insert(parent = "", index = 'end', id = newVal['iD'], text = newVal['iD'] + " : " + newVal['name'], tags = [newVal['iD']])
		filterList[newVal['iD']] = newVal
		filterColor = selectedColor()
		if filterColor != None:
			filterTree.tag_configure(newVal['iD'], background = applyFilter(newVal, colorList[filterColor]['color']))
	
	### Objects ###

filterButtons = ttk.Frame(filterFrame)

replaceFilterButton = ttk.Button(filterButtons, text = "Replace", command = lambda:replaceFilter(selectedFilter(), getFilterBox()))
removeFilterButton  = ttk.Button(filterButtons, text = "Remove", command = lambda:removeFilter(filterTree.selection()))
addFilterButton     = ttk.Button(filterButtons, text = "Add", command = lambda:addFilter(getFilterBox()))

lockFilterCheck = ttk.Checkbutton(filterButtons, var = lockFilter)


	### Formatting ###

filterButtons      .grid(row = 2, column = 0, sticky = tk.NSEW, pady = (10, 0))
replaceFilterButton.grid(row = 0, column = 0, sticky = tk.NSEW)
removeFilterButton .grid(row = 0, column = 1, sticky = tk.NSEW)
addFilterButton    .grid(row = 0, column = 2, sticky = tk.NSEW)

#################################################################### Prefab Frame

	### Objects ###

prefabFrame = ttk.Frame(colorMaker)

	### Formatting ###

prefabFrame.grid(row = 2, column = 2, sticky = tk.NSEW, padx = 5)

################################################################# Prefab Presets

	### Functions ###

def getcolorTemplates():
	for i in os.listdir("userData/colorTemplates"):
		colorTemplateList.append(i.split(".")[0])

def createColorTemplate():
	pathName = simpledialog.askstring("Name", "Preset Name: ")
	if pathName != None:
		writeJson("userData/colorTemplates/" + pathName + ".json", {'colorList':colorList, 'filterList':filterList, 'prefabList':prefabList})

def setColorMaker(path):
	if os.path.exists(path):
		preset = readJson(path)
		for i in colorTree.get_children():
			colorTree.delete(i)
			colorList.pop(i)
		for i in filterTree.get_children():
			filterTree.delete(i)
			filterList.pop(i)
		for i in prefabTree.get_children():
			prefabTree.delete(i)
			prefabList.pop(i)

		for i in preset['colorList']:
			addColor(preset['colorList'][i])
		for i in preset['filterList']:
			addFilter(preset['filterList'][i])
		for i in preset['prefabList']:
			addPrefab(preset['prefabList'][i])

getcolorTemplates()

	### Objects ###

colorTemplateFrame = ttk.Frame(prefabFrame)

colorTemplateMenu = ttk.OptionMenu(colorTemplateFrame, colorTemplateSel, "Color Templates", *colorTemplateList)

colorTemplateAddButton  = ttk.Button(colorTemplateFrame, text = "Load", width = 5, command = lambda: setColorMaker(os.path.join("userData/colorTemplates",colorTemplateSel.get() + ".json")))
colorTemplateSaveButton = ttk.Button(colorTemplateFrame, text = "Save", command = lambda:createColorTemplate())
colorTemplateSeparator = ttk.Separator(colorMaker, orient = 'horizontal')

	### Formatting ###

colorTemplateFrame     .grid(row = 0, column = 0, sticky = tk.N)
colorTemplateSeparator .grid(row = 1, column = 0, sticky = tk.NSEW, columnspan = 3, pady = 5)
colorTemplateMenu      .grid(row = 0, column = 0, sticky = tk.NSEW)
colorTemplateAddButton .grid(row = 0, column = 1, sticky = tk.NSEW)
colorTemplateSaveButton.grid(row = 0, column = 2, sticky = tk.NSEW)

################################################################# Prefab Tree

	### Functions ###

def selectedPrefab():
	return None if prefabTree.focus() == '' else prefabTree.focus()

def updatePrefabTree():
	for i in prefabTree.get_children():
		prefabTree.tag_configure(i, background = evalPaths(prefabList[i]['path']['filters'],colorList[prefabList[i]['path']['colorId']]['color']))

def nextPrefabId():
	iD = 0
	while str(iD) in prefabList.keys():
		iD += 1
	return str(iD)

	### Objects ###

prefabTree = ttk.Treeview(prefabFrame)

	### Formatting ###

prefabTree.grid(row = 1, column = 0, sticky = tk.NSEW)

prefabTree.heading("#0", text = "Prefabs")
prefabTree.column("#0", width = 200)


################################################################# Prefab Box

	### Vars ###

pathFilterAdd = tk.StringVar()
prefabNameVar = tk.StringVar()
prefabIdVar   = tk.StringVar()

prefabIdVar.set(0)

lockFiltersVar = tk.BooleanVar()

	### Functions ###

def setFilterPath(*args):
	if lockFiltersVar.get() == False:
		for i in pathTree.get_children():
			pathTree.delete(i)
		for i in filterTree.selection():
			addPath(i)

def updatePathTree(*args):
	newColor = selectedColor()
	if newColor != None:
		newColor = colorList[newColor]['color']
		for n, i in enumerate(pathTree.get_children()):
			pathTree.item(i, tags = [i])
			newColor = applyFilter(filterList[pathTree.item(i)['text']], newColor)
			pathTree.tag_configure(i, background = newColor)

def selectedPath():
	return None if len(pathTree.selection()) < 1 else filterList[pathTree.item(pathTree.focus())['text']]['iD']

def addPath(filterId):
	if filterId != None and filterId in list(filterList.keys()):
		if len(pathTree.selection()) > 0:
			pathTree.see(pathTree.next(pathTree.insert(parent = "", index = pathTree.index(pathTree.focus()), text = filterId)))
		else:
			pathTree.see(pathTree.next(pathTree.insert(parent = "", index = "end", text = filterId)))
		updatePathTree()
		updatePrefabBox()

def removePath(iDs):
	for i in iDs:
		pathTree.delete(i)
		updatePathTree()
		updatePrefabBox()

def movePath(iDs, direction):
	if direction < 0:
		for i in iDs:
			pathTree.move(i, parent = "", index = pathTree.index(pathTree.next(i)))
	else:
		for i in iDs:
			pathTree.move(i, parent = "", index = pathTree.index(pathTree.prev(i)))
	updatePathTree()
	updatePrefabBox()

def evalPaths(filters, color):
	for i in filters:
		color = applyFilter(filterList[i], color)
	return color

def getPrefabBox():
	if len(colorTree.selection()) < 2:
		colorId = selectedColor()
		if colorId == None:
			color = "#FFFFFF"
		else:
			color = colorList[colorId]['color']
		prefabIdVar.set(nextPrefabId())
		return {"iD":prefabIdVar.get().strip(),"name":prefabNameVar.get().strip(),"path":{"filters":[pathTree.item(i)['text'] for i in pathTree.get_children()],"color":color, "colorId":colorId}}
	else:
		toReturn = []
		for i in colorTree.selection():
			colorId = i
			color = colorList[colorId]['color']
			prefabIdVar.set(nextPrefabId())
			pathListTmp = [pathTree.item(i)['text'] for i in pathTree.get_children()]

			name = colorList[colorId]['name'] + " : "
			for i in pathListTmp:
				name += filterList[i]['name'] + " "

			toReturn.append({"iD":prefabIdVar.get().strip(),"name":name,"path":{"filters":pathListTmp,"color":color, "colorId":colorId}})
			prefabList[prefabIdVar.get()] = {}
		print(toReturn)
		return toReturn

def setPrefabBox(newVal):
	prefabIdVar.set(newVal['iD'])
	prefabNameVar.set(newVal['name'])
	for i in pathTree.get_children():
		pathTree.delete(i)
	for i in newVal['path']['filters']:
		addPath(i)
	colorTree.focus(newVal['path']['colorId'])
	updatePrefabBox()

def updatePrefabBox(copy = False):
	toEval = [pathTree.item(i)['text'] for i in pathTree.get_children()]
	color = selectedColor()
	if color != None:
		currentColor = evalPaths(toEval, colorList[color]['color'])
		prefabView.configure(bg = currentColor)
		if copy:
			r.clipboard_clear()  # clear clipboard contents
			r.clipboard_append(currentColor)
	updatePathTree()

	### Objects ###

prefabBox = ttk.Frame(prefabFrame)
pathFrame  = ttk.Frame(prefabBox)

prefabInfo = ttk.LabelFrame(prefabBox, text = "ID : Name")

pathTree = ttk.Treeview(pathFrame, height = 5)

prefabSeparator = ttk.Label(prefabInfo, text = " : ")

prefabView          = tk.Button(prefabBox, relief = "sunken", command = lambda:updatePrefabBox(copy = True))
addPathButton       = ttk.Button(pathFrame, text = "+", width = 2, command = lambda:addPath(selectedPath()))
removePathButton    = ttk.Button(pathFrame, text = "-", width = 2, command = lambda:removePath(pathTree.selection()))
movePathUpButton    = ttk.Button(pathFrame, text = "^", width = 2, command = lambda:movePath(pathTree.selection(), 1))
movePathDownButton  = ttk.Button(pathFrame, text = "v", width = 2, command = lambda:movePath(pathTree.selection(), -1))

filterAddEntry = ttk.Entry(pathFrame, textvariable = pathFilterAdd, width = 5)

prefabId       = ttk.Spinbox(prefabInfo, textvariable = prefabIdVar, width = 5, from_ = 0, to = 100, increment = 1, wrap = False)
prefabName     = ttk.Entry(prefabInfo, textvariable = prefabNameVar, width = 15)
prefabBoxAdd        = ttk.Button(prefabInfo, text = "Add", command = lambda:addPrefab(getPrefabBox()), width = 10)


lockFilters = ttk.Checkbutton(pathFrame, var = lockFiltersVar)

	### Formatting ###

prefabBox          .grid(row = 3, column = 0, sticky = tk.NSEW)
prefabView         .grid(row = 0, column = 0, sticky = tk.NSEW, ipady = 67, ipadx = 43)

pathFrame          .grid(row = 0, column = 1, sticky = tk.NSEW)
pathTree           .grid(row = 0, column = 0, sticky = tk.NSEW, columnspan = 4, rowspan = 2)
filterAddEntry     .grid(row = 2, column = 1, sticky = tk.NSEW)
addPathButton      .grid(row = 2, column = 2, sticky = tk.NSEW)
removePathButton   .grid(row = 2, column = 3, sticky = tk.NSEW)
movePathUpButton   .grid(row = 0, column = 4, sticky = tk.NSEW)
movePathDownButton .grid(row = 1, column = 4, sticky = tk.NSEW)
lockFilters         .grid(row = 2, column = 4, sticky = tk.NSEW, padx = (5,0))

prefabInfo         .grid(row = 1, column = 0, sticky = tk.NSEW, columnspan = 2)
prefabId           .grid(row = 0, column = 0, sticky = tk.NSEW)
prefabName         .grid(row = 0, column = 2, sticky = tk.NSEW)
prefabSeparator    .grid(row = 0, column = 1, sticky = tk.NSEW)
prefabBoxAdd       .grid(row = 0, column = 3, sticky = tk.NSEW)

pathTree.column("#0", width = 10)
pathTree.heading("#0", text = "Path")

	### Misc ###

filterTree.bind("<<TreeviewSelect>>", lambda x:[setFilterPath(), updatePrefabBox()])
prefabBoxAdd.bind("<Return>", lambda x :addPrefab(getPrefabBox()))
filterAddEntry.bind("<Return>", lambda x:addPath(filterAddEntry.get().strip()))

################################################################# Prefab Buttons

	### Functions ###

def addPrefab(val):
	if type(val) == dict:
		if val != None and val['iD'] != "" and val['path']['colorId'] != None:
			prefabTree.insert(parent = "", index = "end", id = val['iD'], text = val['iD'] + " : " + val['name'], tags = [val['iD']])
			prefabTree.tag_configure(val['iD'], background = evalPaths(val['path']['filters'], val['path']['color']))
			prefabList[val['iD']] = val
	else:
		for i in val:
			prefabTree.insert(parent = "", index = "end", id = i['iD'], text = i['iD'] + " : " + i['name'], tags = [i['iD']])
			prefabTree.tag_configure(i['iD'], background = evalPaths(i['path']['filters'], i['path']['color']))
			prefabList[i['iD']] = i

def removePrefab(iDs):
	for i in iDs:
		prefabTree.delete(i)
		prefabList.pop(i)

def replacePrefab(iD, newVal):
	if iD != None:
		newVal['iD'] = iD
		prefabTree.item(iD, text = newVal['iD'] + " : " + newVal['name'])
		prefabList[iD] = newVal
		prefabTree.tag_configure(iD, background = evalPaths(newVal['path']['filters'],newVal['path']['color']))

	### Objects ###

prefabButtons       = ttk.Frame(prefabFrame)

replacePrefabButton = ttk.Button(prefabButtons, text = "Replace", command = lambda:replacePrefab(selectedPrefab(), getPrefabBox()))
removePrefabButton  = ttk.Button(prefabButtons, text = "Remove", command = lambda:removePrefab(prefabTree.selection()))
addPrefabButton     = ttk.Button(prefabButtons, text = "Add", command = lambda:addPrefab(getPrefabBox()))

	### Formatting ###

prefabButtons      .grid(row = 2, column = 0, sticky = tk.NSEW, pady = (10, 0))
replacePrefabButton.grid(row = 0, column = 0, sticky = tk.NSEW)
removePrefabButton .grid(row = 0, column = 1, sticky = tk.NSEW)
addPrefabButton    .grid(row = 0, column = 2, sticky = tk.NSEW)

prefabTree.bind("<Double-1>", lambda x:setPrefabBox(prefabList[selectedPrefab()]))

####################################################################### File Maker

	### Vars ###

fileVar = {}

	### Functions ###

	### Objects ###

fileMaker = ttk.Frame(root)

fileMakerSep = ttk.Separator(root, orient = 'vertical')

	### Formatting

fileMaker   .grid(row = 0, column = 2, sticky = tk.NSEW)
fileMakerSep.grid(row = 0, column = 1, sticky = tk.NSEW, padx = 5)

####################################################################### File Presets

	### Vars ###

filePresetList = []
filePresetSel  = tk.StringVar()

	### Functions ###

def setFileMaker(preset):
	pass

def createFileMakerPreset():
	pass

def getFileMakerPresets():
	pass

	### Objects ###
filePresetFrame = ttk.Frame(fileMaker)

filePresetMenu = ttk.OptionMenu(filePresetFrame, filePresetSel, "File Templates", *filePresetList)

filePresetLoad = ttk.Button(filePresetFrame, text = "Load")
filePresetSave = ttk.Button(filePresetFrame, text = "Save")

filePresetSep = ttk.Separator(fileMaker, orient = "horizontal")

	### Formatting ###

filePresetFrame.grid(row = 0, column = 0, sticky = tk.NSEW, columnspan = 3)
filePresetMenu .grid(row = 0, column = 0, sticky = tk.NSEW)
filePresetLoad .grid(row = 0, column = 1, sticky = tk.NSEW)
filePresetSave .grid(row = 0, column = 2, sticky = tk.NSEW)

filePresetSep.grid(row = 1, column = 0, sticky = tk.NSEW, columnspan = 3, pady = 5)

####################################################################### Label Frame

	### Vars ###

labelNameVar   = tk.StringVar()
labelPrefabVar = tk.StringVar()

	### Functions ###

def addLabel(name, prefab):
	pass

def replaceLabel(name, newName):
	pass

def removeLabel(name):
	pass

def updateLabelBox():
	pass

	### Objects ###

labelFrame = ttk.Frame(fileMaker)
labelBox   = ttk.Frame(labelFrame)

labelTree = ttk.Treeview(labelFrame, height = 9, style = "labelTree.Treeview")

labelNameLabel   = ttk.Label(labelBox, text = "Name: ")
labelPrefabLabel = ttk.Label(labelBox, text = "Prefab: ")

labelNameEntry   = ttk.Entry(labelBox, width = 10)
labelPrefabEntry = ttk.Entry(labelBox, width = 10)

labelAddButton     = ttk.Button(labelBox, text = "Add")
labelRemoveButton  = ttk.Button(labelBox, text = "Remove")
labelReplaceButton = ttk.Button(labelBox, text = "Replace")

	### Formatting ###

labelFrame.grid(row = 2, column = 0, sticky = tk.NSEW, padx = 5)
labelTree .grid(row = 0, column = 0, sticky = tk.NSEW)

labelBox.grid(row = 1, column = 0, sticky = tk.NSEW)

labelNameLabel  .grid(row = 0, column = 0, sticky = tk.NSEW)
labelPrefabLabel.grid(row = 1, column = 0, sticky = tk.NSEW)
labelNameEntry  .grid(row = 0, column = 1, sticky = tk.NSEW)
labelPrefabEntry.grid(row = 1, column = 1, sticky = tk.NSEW)

labelAddButton    .grid(row = 2, column = 0, sticky = tk.NSEW, columnspan = 2)
labelRemoveButton .grid(row = 3, column = 0, sticky = tk.NSEW)
labelReplaceButton.grid(row = 3, column = 1, sticky = tk.NSEW)

labelTree.column("#0", width = 50)
labelTree.heading("#0", text = "Labels")

labelTree.insert(parent = "", index = "end", text = "Remove")
labelTree.insert(parent = "", index = "end", text = "Hi")
labelTree.insert(parent = "", index = "end", text = "Hi")
labelTree.insert(parent = "", index = "end", text = "Hi")
labelTree.insert(parent = "", index = "end", text = "Hi")

####################################################################### Mod Frame

	### Vars ###

modHVar = tk.IntVar()
modSVar = tk.IntVar()
modLVar = tk.IntVar()
modAVar = tk.IntVar()

modViewBgColor1 = "#C9C9C9"
modViewBgColor2 = "#F3F6F3"

	### Functions ###

def addMod(val):
	pass

def removeMod(name):
	pass

def replaceVal(name, newVal):
	pass

def applyMod(val, color):
	pass

def updateModTree(*args):
	pass

def setModBox(val):
	pass

def updateModBox(*args):
	pass

def roundModSliders(*args):
	modHVar.set(round(modHVar.get()))
	modSVar.set(round(modSVar.get()))
	modLVar.set(round(modLVar.get()))
	modAVar.set(round(modAVar.get()))

	### Objects ###

modFrame   = ttk.Frame(fileMaker)
modBox     = ttk.Frame(modFrame)
modSliders = ttk.LabelFrame(modBox, text = "Sliders")

modTree = ttk.Treeview(modFrame, height = 12)

modView = tk.Canvas(modBox, width = 25, height = 167, bg = "black")

modNameEntry = ttk.Entry(modBox, width = 8)

modAddButton     = ttk.Button(modBox, text = "Add", width = 5)
modRemoveButton  = ttk.Button(modBox, text = "Remove")
modReplaceButton = ttk.Button(modBox, text = "Replace", width = 8)

modLabelH = ttk.Label(modSliders, text = "H")
modLabelS = ttk.Label(modSliders, text = "S")
modLabelL = ttk.Label(modSliders, text = "L")
modLabelA = ttk.Label(modSliders, text = "A")

modEntryH = ttk.Entry(modSliders, textvariable = modHVar, width = 4)
modEntryS = ttk.Entry(modSliders, textvariable = modSVar, width = 4)
modEntryL = ttk.Entry(modSliders, textvariable = modLVar, width = 4)
modEntryA = ttk.Entry(modSliders, textvariable = modAVar, width = 4)

modSliderH = ttk.Scale(modSliders, from_ = 255, to = -255, var = modHVar, orient = "vertical", command = roundModSliders, length = 136)
modSliderS = ttk.Scale(modSliders, from_ = 255, to = -255, var = modSVar, orient = "vertical", command = roundModSliders)
modSliderL = ttk.Scale(modSliders, from_ = 255, to = -255, var = modLVar, orient = "vertical", command = roundModSliders)
modSliderA = ttk.Scale(modSliders, from_ = 255, to = -255, var = modAVar, orient = "vertical", command = roundModSliders)

	### Formatting ###

modFrame.grid(row = 2, column = 1, sticky = tk.NSEW, padx = 5)

modTree.grid(row = 0, column = 0, sticky = tk.NSEW)

modBox          .grid(row = 1, column = 0, sticky = tk.NSEW)
modView         .grid(row = 0, column = 0, sticky = tk.NSEW, columnspan = 2)
modNameEntry    .grid(row = 1, column = 0, sticky = tk.NSEW)
modAddButton    .grid(row = 1, column = 1, sticky = tk.NSEW)
modRemoveButton .grid(row = 2, column = 0, sticky = tk.NSEW, columnspan = 2)
modReplaceButton.grid(row = 2, column = 2, sticky = tk.NSEW)

modSliders.grid(row = 0, column = 2, sticky = tk.NSEW, rowspan = 3)
modLabelH .grid(row = 0, column = 0, sticky = tk.NSEW)
modLabelS .grid(row = 0, column = 1, sticky = tk.NSEW)
modLabelL .grid(row = 0, column = 2, sticky = tk.NSEW)
modLabelA .grid(row = 0, column = 3, sticky = tk.NSEW)
modEntryH .grid(row = 2, column = 0, sticky = tk.NSEW)
modEntryS .grid(row = 2, column = 1, sticky = tk.NSEW)
modEntryL .grid(row = 2, column = 2, sticky = tk.NSEW)
modEntryA .grid(row = 2, column = 3, sticky = tk.NSEW)
modSliderH.grid(row = 1, column = 0, sticky = tk.NSEW)
modSliderS.grid(row = 1, column = 1, sticky = tk.NSEW)
modSliderL.grid(row = 1, column = 2, sticky = tk.NSEW)
modSliderA.grid(row = 1, column = 3, sticky = tk.NSEW)

modTree.column("#0", width = 50)
modTree.heading("#0", text = "Modifiers")

# for i in range

####################################################################### Dest Frame

	### Vars ###

values     = readJson("programData/files.json")
fileList   = values['colors']
valueList  = values['values']
folderList = readJson("programData/folders.json")

	### Functions ###

def applyConnection(connection):
	pass

def clearConnection(connection):
	pass

def createSkin():
	pass

def loadSkin():
	pass

def updateDestTree():
	pass

	### Objects ###

destFrame = ttk.Frame(fileMaker)

folderTree = ttk.Treeview(destFrame, height = 10, style = "folderTree.Treeview")
fileTree   = ttk.Treeview(destFrame, height = 20)

applyConnectionButton = ttk.Button(destFrame, text = "Apply")
clearConnectionButton = ttk.Button(destFrame, text = "Clear")
loadSkinButton        = ttk.Button(destFrame, text = "Load Skin")
createFileButton      = ttk.Button(destFrame, text = "Create Skin")

	### Formatting ###

destFrame .grid(row = 2, column = 2, sticky = tk.NSEW, padx = 5)
folderTree.grid(row = 0, column = 2, sticky = tk.NSEW, rowspan = 2)
fileTree  .grid(row = 0, column = 0, sticky = tk.NSEW, columnspan = 2)

applyConnectionButton.grid(row = 1, column = 0, sticky = tk.NSEW)
clearConnectionButton.grid(row = 1, column = 1, sticky = tk.NSEW)
loadSkinButton       .grid(row = 2, column = 2, sticky = tk.NSEW, ipady = 5)
createFileButton     .grid(row = 2, column = 0, columnspan = 2, sticky = tk.NSEW, ipady = 5)

folderTree.column("#0", width = 125)
fileTree  .column("#0", width = 200)
folderTree.heading("#0", text = "Folder")
fileTree  .heading("#0", text = "File")

for i in folderList:
	folderTree.insert(parent = "", index = "end", iid = i, text = i)
for i in fileList:
	fileTree.insert(parent = "", index = "end", iid = i, text = i)

r.mainloop()





# File Maker Structure
"""
{
	"Background":"#44444444"
	"overrides":{
		"Oscillator":{
			"Backgroud":{"label":"","modifier":""}
		}
	}
} 

# View Structure
{
	"main":{stuffaaaaaaaaaaaaaaa}
}
"""