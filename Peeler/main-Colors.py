import colorzero as cz
import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser

main = tk.Tk()
root = ttk.Frame(main)
root.grid(row = 0, column = 0, padx = 10, pady = 10)

##################################################### Main Blocking ###

colorFrame = ttk.Frame(root) # Houses all color manipulation
colorFrame.grid(row = 0, column = 0, sticky = tk.NSEW)

fileFrame = ttk.Frame(root) # Houses all .vitalskin creation
fileFrame.grid(row = 0, column = 1, sticky = tk.NSEW)

	### Variables ###

colorList = {}
filterList = {}
prefabList = {}

#######################################################################

####################################################### Color Frame ###

### Treeviews ###
colors = ttk.Treeview(colorFrame)
filters = ttk.Treeview(colorFrame)
prefabs = ttk.Treeview(colorFrame)

colors.column("#0", width = 150)
filters.column("#0", width = 150)
prefabs.column("#0", width = 150)

colors.heading("#0", text = "Colors")
filters.heading("#0", text = "Filters")
prefabs.heading("#0", text = "Prefabs")

colors.grid(row = 0, column = 0, sticky = tk.NSEW)
filters.grid(row = 0, column = 1, sticky = tk.NSEW)
prefabs.grid(row = 0, column = 2, sticky = tk.NSEW)

	### Treeview Controls ###

colorButtons = ttk.Frame(colorFrame)
colorButtons.grid(row = 1, column = 0, sticky = tk.NSEW)

filterButtons = ttk.Frame(colorFrame)
filterButtons.grid(row = 1, column = 1, sticky = tk.NSEW)

prefabButtons = ttk.Frame(colorFrame)
prefabButtons.grid(row = 1, column = 2, sticky = tk.NSEW)

	### Color Creator ###

colorCreator = ttk.Frame(colorFrame)
colorCreator.grid(row = 2, column = 0, sticky = tk.NSEW)

color = tk.StringVar()
color.set("#FFFFFF")

colorReadout = ttk.Frame(colorCreator)
colorReadout.grid(row = 1, column = 0, sticky = tk.EW)

def browseColor(*args):
	newColor = colorchooser.askcolor()
	if newColor[0] != None:
		color.set(newColor[1])

		c = cz.Color(newColor[1])
		rgb = c.rgb_bytes
		r.set(rgb[0])
		g.set(rgb[1])
		b.set(rgb[2])

		updateColor()

colorRead = ttk.Entry(colorReadout, textvariable = color, width = 8)
colorRead.grid(row = 0, column = 0, sticky = tk.EW)

colorBrowse = ttk.Button(colorReadout, text = "B", command = browseColor, width = 1)
colorBrowse.grid(row = 0, column = 1)

	### Sliders ###

colorSliders = ttk.LabelFrame(colorCreator, text = "Color Vals")
colorSliders.grid(row = 0, column = 1, sticky = tk.NSEW, rowspan = 2)

r = tk.IntVar()
g = tk.IntVar()
b = tk.IntVar()

r.set(189)
g.set(106)
b.set(133)

def roundSliders(*args):
	r.set(round(r.get()))
	g.set(round(g.get()))
	b.set(round(b.get()))

def updateColor(*args):
	roundSliders()

	newColor = getColor()['color']
	colorView.configure(bg = color.get())
	color.set(newColor)

	for i in colors.get_children():
		colors.tag_configure(i, background = colorList[i]['color'])

colorView = tk.Button(colorCreator, bg = color.get(), activebackground = color.get(), relief = 'sunken', command = updateColor)
colorView.grid(row = 0, column = 0, sticky = tk.NSEW, ipadx = 30, ipady = 52)

vals = [r,g,b]
names = ['r','g','b']
i = 0

for name, val in zip(names, vals):
	ttk.Label(colorSliders, text = name.title()) .grid(row = 0, column = i, sticky = tk.N)
	ttk.Scale(colorSliders, orient = 'vertical', to = 0, from_ = 255, var = val, command = updateColor) .grid(row = 1, column = i, sticky = tk.N)
	ttk.Entry(colorSliders, textvariable = val, width = 4) .grid(row = 2, column = i, sticky = tk.N)
	i+=1

	### Name & ID ###

colorLabel = ttk.LabelFrame(colorCreator, text = "Name : ID")
colorLabel.grid(row = 3, column = 0, columnspan = 2, sticky = tk.N)

colorName = tk.StringVar()
colorId = tk.StringVar()

ttk.Entry(colorLabel, textvariable = colorName, width = 10) .grid(row = 0, column = 0, sticky = tk.NSEW)
ttk.Label(colorLabel, text = " : ") .grid(row = 0, column = 1, sticky = tk.NSEW)
ttk.Entry(colorLabel, textvariable = colorId, width = 10) .grid(row = 0, column = 2, sticky = tk.NSEW)

def getColor(*args):
	def getC(var):
		return var.get()*(1/255)
	c = cz.Color(getC(r), getC(g), getC(b))
	return {"name":colorName.get().strip(), "color":str(c), "iD":colorId.get().strip()}

def addColor(iD, name, color):
	if iD not in colorList.keys():
		colorList[iD] = {"name":name, "color":color, "iD":iD}
		colors.insert(parent = "", index = 'end', id = iD, text = iD + " : " + name, tags = [iD])
		colors.tag_configure(iD, background = color)

def setColor(*args):
	if len(colors.selection()) > 0:
		values = colorList[colors.selection()[0]]
		colorName.set(values['name'])
		colorId.set(values['iD'])
		colorRead.delete(0,tk.END)
		colorRead.insert(0,values['color'])
		c = cz.Color(values['color']).rgb_bytes
		r.set(c[0])
		g.set(c[1])
		b.set(c[2])
		updateDisplays()

colorView.configure(bg = getColor()['color'])
color.set(getColor()['color'])

ttk.Button(colorLabel, text = "ADD", command = lambda : addColor(colorId.get().strip(), colorName.get().strip(), getColor()['color'])) .grid(row = 1, column = 0, columnspan = 3, sticky = tk.NSEW)

	#### Filter Creator ###

filterCreator = ttk.Frame(colorFrame)
filterCreator.grid(row = 2, column = 1, sticky = tk.NSEW)

filterPreview = tk.StringVar()
filterPreview.set("#FFFFFF")

h = tk.IntVar()
s = tk.IntVar()
l = tk.IntVar()

h.set(0)
s.set(0)
l.set(0)

filterName = tk.StringVar()
filterId = tk.StringVar()

filterVals = [h,s,l]
filterNames = ['h','s','l']

def applyFilter(color, filter_):
	def getC(val):
		return val*(1/255)
	c = cz.Color(color)
	c = c + cz.Hue(getC(filter_['h']))
	c = c + cz.Saturation(getC(filter_['s']))
	c = c + cz.Lightness(getC(filter_['l']))

	return str(c)

def getFilter():
	return {"name":filterName.get().strip(), "h":h.get(), "s":s.get(), "l":l.get(), "iD":filterId.get().strip(), "color":"#FFFFFF"}

def roundFilter(*args):
	s.set(round(s.get()))
	h.set(round(h.get()))
	l.set(round(l.get()))

def updateFilter(*args):
	roundFilter()
	if len(colors.selection()) > 0:
		selectedColor = colorList[colors.selection()[0]]['color']
		applied = applyFilter(selectedColor, getFilter())
		filterPreview.set(applied)
		filterView.configure(bg = applied)
		for i in filterList.keys():
			filters.tag_configure(i, background = applyFilter(selectedColor, filterList[i]))

def addFilter(iD, name, h, s, l):
	if iD not in filterList.keys():
		filterList[iD] = {"name":name, "iD":iD, "h":h, "s":s, "l":l, "color":"#FFFFF"}
		filters.insert(parent = "", index = "end", id = iD, text = iD + " : " + name, tags = [iD])

def setFilter(*args):
	if len(filters.selection()) > 0:
		values = filterList[filters.selection()[0]]
		filterName.set(values['name'])
		filterId.set(values['iD'])
		h.set(values['h'])
		s.set(values['s'])
		l.set(values['l'])
		updateDisplays()

filterView = tk.Button(filterCreator, bg = filterPreview.get(), activebackground = filterPreview.get(), relief = 'sunken', command = updateFilter)
filterView.grid(row = 0, column = 0, sticky = tk.NSEW, ipadx = 30, ipady = 52)

filterSliders = ttk.LabelFrame(filterCreator, text = "Filter Vals")
filterSliders.grid(row = 0, column = 1, sticky = tk.NSEW)

i = 0

for name, val in zip(filterNames, filterVals):
	ttk.Label(filterSliders, text = name.title()) .grid(row = 0, column = i, sticky = tk.N)
	ttk.Scale(filterSliders, orient = 'vertical', to = -255, from_ = 255, var = val, command = updateFilter) .grid(row = 1, column = i, sticky = tk.N)
	ttk.Entry(filterSliders, textvariable = val, width = 4) .grid(row = 2, column = i, sticky = tk.N)
	i+=1

filterLabel = ttk.LabelFrame(filterCreator, text = "Name : ID")
filterLabel.grid(row = 3, column = 0, columnspan = 2, sticky = tk.N)

ttk.Entry(filterLabel, textvariable = filterName, width = 10) .grid(row = 0, column = 0, sticky = tk.NSEW)
ttk.Label(filterLabel, text = " : ") .grid(row = 0, column = 1, sticky = tk.NSEW)
ttk.Entry(filterLabel, textvariable = filterId, width = 10) .grid(row = 0, column = 2, sticky = tk.NSEW)

ttk.Button(filterLabel, text = "Add", command = lambda : addFilter(filterId.get().strip(), filterName.get().strip(), h.get(), s.get(), l.get())) .grid(row = 1, column = 0, columnspan = 3, sticky = tk.NSEW)

	### Prefab Creator ###

prefabCreator = ttk.Frame(colorFrame)
prefabCreator.grid(row = 2, column = 2, sticky = tk.NSEW)

pathList = ttk.Treeview(prefabCreator, height = 5)
pathList.grid(row = 0, column = 1, sticky = tk.NSEW)

pathList.column("#0", width = 25)
pathList.heading("#0", text = "Path")

pathButtons = ttk.Frame(prefabCreator)
pathButtons.grid(row = 1, column = 1, sticky = tk.N)

prefabLabel = ttk.LabelFrame(prefabCreator, text = "Name : ID")
prefabLabel.grid(row = 2, column = 0, columnspan = 2, sticky = tk.N)

def addPathFilter(filterId):
	lockFilter.set(1)
	if filterId == "ps":
		if len(pathList.selection()) > 0:
			filterId = pathList.item(pathList.selection()[0], 'text').strip()
		else:
			return
	print(filterId)
	if filterId in filterList.keys():
		pathList.insert(parent = "", index = 'end', text = filterId)
		updatePrefab()

def deletePathFilter():
	lockFilter.set(1)
	for i in pathList.selection():
		pathList.delete(i)
	updatePrefab()

def movePathFilter(amount):
	lockFilter.set(1)
	if len(pathList.selection()) > 0:
		if amount == 1:
			for i in pathList.selection():
				pathList.move(i, parent = "", index = pathList.index(pathList.prev(i)))
		else:
			for i in pathList.selection():
				pathList.move(i, parent = "", index = pathList.index(pathList.next(i)))
	updatePrefab()

filterAdd = tk.StringVar()

ttk.Button(pathButtons, text = "+", width = 1, command = lambda:addPathFilter("ps")) .grid(row = 0, column = 0, sticky = tk.NSEW)
ttk.Button(pathButtons, text = "-", width = 1, command = deletePathFilter) .grid(row = 0, column = 1, sticky = tk.NSEW)
ttk.Button(pathButtons, text = "^", width = 1, command = lambda:movePathFilter(1)) .grid(row = 0, column = 2, sticky = tk.NSEW)
ttk.Button(pathButtons, text = "v", width = 1, command = lambda:movePathFilter(-1)) .grid(row = 0, column = 3, sticky = tk.NSEW)
ttk.Entry(pathButtons, textvariable = filterAdd, width = 5) .grid(row = 1, column = 0, columnspan = 3, sticky = tk.NSEW)
ttk.Button(pathButtons, text = "^", width = 1, command = lambda:addPathFilter(filterAdd.get().strip())) .grid(row = 1, column = 3, sticky = tk.NSEW)

prefabName = tk.StringVar()
prefabId = tk.StringVar()

def evalPrefab(path, colorId):
	newColor = colorList[colorId]['color']
	for i in path:
		newColor = applyFilter(newColor, filterList[i])
	return newColor

def getPrefab(*args):
	color = colors.selection()[0]
	filters_ = list(filters.selection())
	path = {'iD':prefabId.get().strip(), 'name':prefabName.get().strip(), 'colorId':color, 'filters':filters_}
	return path

def setPrefab(*args):
	gottenPrefab = prefabList[prefabs.selection()[0]]
	prefabName.set(gottenPrefab['name'])
	prefabId.set(gottenPrefab['iD'])
	for i in pathList.get_children():
		pathList.delete(i)
	lockFilter.set(1)
	for i in gottenPrefab['filters']:
		pathList.insert(parent = "", index = 'end', text = i, tags = [i])
	updateDisplays()

def addPrefab(iD, name, path, colorId):
	if colorId == "cs":
		if not len(colors.selection()) > 0:
			colorId = '#FFFFFF'
		else:
			colorId = colors.selection()[0]
	prefabs.insert(parent = "", index = 'end', id = iD, text = iD + " : " + name, tags = [iD])
	prefabs.tag_configure(iD, background = evalPrefab(path, colorId))
	prefabList[iD] = {'iD':iD, 'name':name, 'colorId':colorId, 'filters':path}

lockFilter = tk.BooleanVar()
lockFilter.set(0)

def updatePrefab(*args):
	if not lockFilter.get():
		for i in pathList.get_children():
			pathList.delete(i)
		for i in filters.selection():
			pathList.insert(parent = "", index = 'end', text = i)

	if len(colors.selection()) > 0:
		nextColor = colorList[colors.selection()[0]]['color']
		for n, i in enumerate(pathList.get_children()):
			try:
				nextColor = applyFilter(nextColor, filterList[pathList.item(i,'text')])
				pathList.item(i, tags = [n])
				pathList.tag_configure(n, background = nextColor)
			except KeyError:
				pathList.delete(i)
		prefabView.configure(bg = evalPrefab([pathList.item(i, 'text') for i in pathList.get_children()], colors.selection()[0]))
	for i in prefabs.get_children():
		prefabs.tag_configure(i, background = evalPrefab(prefabList[i]['filters'], prefabList[i]['colorId']))

prefabView = tk.Button(prefabCreator, relief = 'sunken', command = updatePrefab)
prefabView.grid(row = 0, column = 0, sticky = tk.NSEW, ipadx = 30, ipady = 66, rowspan = 2)

ttk.Entry(prefabLabel, textvariable = prefabName, width = 10) .grid(row = 0, column = 0, sticky = tk.NSEW)
ttk.Label(prefabLabel, text = " : ") .grid(row = 0, column = 1, sticky = tk.NSEW)
ttk.Entry(prefabLabel, textvariable = prefabId, width = 10) .grid(row = 0, column = 2, sticky = tk.NSEW)

ttk.Button(prefabLabel, text = "Add", command = lambda:addPrefab(prefabId.get().strip(), prefabName.get().strip(), [pathList.item(i, 'text') for i in pathList.get_children()], "cs")) .grid(row = 1, column = 0, columnspan = 3, sticky = tk.NSEW)

	### Other ###

def updateDisplays(*args):
	updateFilter()
	updateColor()
	updatePrefab()

colors.bind("<<TreeviewSelect>>", updateDisplays)
filters.bind("<<TreeviewSelect>>", updateDisplays)
colors.bind("<Double-1>", setColor)
filters.bind("<Double-1>", setFilter)
prefabs.bind("<Double-1>", setPrefab)

		## Functions ##
def checkSeleck(tree):
	return len(tree.selection()) > 0

def remove(tree, list_):
	if checkSeleck(tree):
		for i in tree.selection():
			tree.delete(i)
			list_.pop(i)
	updateDisplays()
def replaceColor(iD, value):
	if iD == "cs":
		if len(colors.selection()) > 0:
			iD = colors.selection()[0]
		else:
			return
	colors.item(iD, text = iD + " : " + value['name'], tags = [iD])
	colorList[iD] = value 
	updateDisplays()

def replaceFilter(iD, value):
	if iD == "fs":
		if len(filters.selection()) > 0:
			iD = filters.selection()[0]
		else:
			return
	filters.item(iD, text = iD + " : " + value['name'], tags = [iD])
	filterList[iD] = value
	updateDisplays()

def replacePrefab(iD, value):
	if iD == "ps":
		if len(prefabs.selection()) > 0:
			iD = prefabs.selection()[0]
		else:
			return
	prefabs.item(iD, text = iD + " : " + value['name'], tags = [iD])
	prefabList[iD] = value
	updateDisplays()

updateDisplays()

		## Buttons ##

ttk.Button(colorButtons, text = "Remove", command = lambda:remove(colors, colorList)) .grid(row = 0, column = 0, sticky = tk.W)
ttk.Button(colorButtons, text = "Replace", command = lambda:replaceColor("cs", getColor())) .grid(row = 0, column = 1, sticky = tk.E)

ttk.Button(filterButtons, text = "Remove", command = lambda:remove(filters, filterList)) .grid(row = 0, column = 0, sticky = tk.NSEW)
ttk.Button(filterButtons, text = "Replace", command = lambda:replaceFilter("fs", getFilter())) .grid(row = 0, column = 1, sticky = tk.NSEW)
ttk.Checkbutton(filterButtons, var = lockFilter) .grid(row = 0, column = 3, sticky = tk.W)

ttk.Button(prefabButtons, text = "Remove", command = lambda:remove(prefabs, prefabList)) .grid(row = 0, column = 0, sticky = tk.NSEW)
ttk.Button(prefabButtons, text = "Replace", command = lambda:replacePrefab("ps", getPrefab())) .grid(row = 0, column = 1, sticky = tk.NSEW)

addColor("1","Red","#d63e43")  
addColor("2","Blue","#4f69b0") 

addFilter("1","Lighter",0,0,20)
addFilter("2","Darker",0,0,-20)
addFilter("3","Pass",0,0,0)

# addPrefab(iD, name, path, colorId)
addPrefab("1", "Dark Blue", ["2","2","2"], "2")

main.mainloop()