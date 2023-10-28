import os
import math
import json

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
# from PIL import Image, ImageTk

import expression

class Exprevo(ttk.Frame):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.main_expr = expression.Expression("x")
		self.offspring_count = tk.IntVar()

		self.image_frame = ttk.Frame(self)
		self.hover_equation_var = tk.StringVar()
		self.equation_entry = ttk.Entry(self, width=100, textvariable=self.hover_equation_var)
		self.big_preview = ttk.Label(self, text="hi")

		self.offspring_count.set(9)
		self.images = []
		self.larger_images = []
		self.expressions = []
		self.per_row = 3.0

		self.button_frame = ttk.Frame(self)
		self.from_json_button = ttk.Button(self.button_frame, text="From JSON", command=self.from_json)
		self.to_json_button = ttk.Button(self.button_frame, text="To JSON", command=self.to_json)

		self.generate_offspring()

	def from_json(self):
		file = fd.askopenfilename(filetypes=[("JSON","*.json")])
		if file:
			with open(file, "r") as f:
				json_dict = json.loads(f.read())
				self.main_expr.from_json(json_dict) 
				self.generate_offspring()

	def to_json(self):
		file = fd.asksaveasfile(defaultextension=".JSON")
		if file:
			with file as f:
				f.write(json.dumps(self.main_expr.to_json()))

	def handle_button_hover(self, n):
		self.hover_equation_var.set(self.expressions[n])

		self.big_preview.configure(image=self.larger_images[n])
		# self.big_preview.image=self.larger_images[n]

	def prime_selection(self, n):
		self.main_expr = self.expressions[n]
		self.generate_offspring()

	def generate_offspring(self):
		# delete children
		children = self.image_frame.winfo_children()
		for child in children:
			child.destroy()
		self.images = []
		self.larger_images = []
		self.expressions = []
		self.hover_equation_var.set(str(self.main_expr))

		offspring = [self.main_expr] + [self.main_expr.copy() for i in range(self.offspring_count.get()-1)]
		self.main_expr.render_to("image_cache",0)
		for n, child in enumerate(offspring):

			if n != 0:
				child.mutate()
			self.expressions.append(child)

			image_path = child.render_to("image_cache",n+1)

			image = tk.PhotoImage(file=image_path)
			preview_image = image.zoom(3,3)

			self.images.append(image)
			self.larger_images.append(preview_image)

			button = tk.Button(self.image_frame, text=n, image=image, command=lambda n=n: self.prime_selection(n))

			pos_index = (1.0*n)/self.per_row
			row = math.floor(pos_index)*1.0
			column = (pos_index - row)*self.per_row
			row=int(row)
			column = round(column)
			button.grid(row=row,column=column,sticky=tk.NSEW)
			button.bind("<Enter>", lambda a, n=n: self.handle_button_hover(n))

			tk.Grid.columnconfigure(self.image_frame, index=column, weight=1)
			tk.Grid.rowconfigure(self.image_frame, index=row, weight=1)
		self.handle_button_hover(0)

	def grid(self, *args, **kwargs):
		tk.Grid.columnconfigure(self,index=0, weight=1)
		tk.Grid.rowconfigure(self,index=0, weight=1)

		super().grid(*args, **kwargs)

		self.big_preview.grid(row=0,column=1)
		self.image_frame.grid(row=0,column=0,sticky=tk.N)
		self.equation_entry.grid(row=1,column=0,sticky=tk.NSEW)

		self.button_frame.grid(row=1, column=1)
		self.to_json_button.grid(row=0, column=0)
		self.from_json_button.grid(row=0, column=1)

root = tk.Tk()
exprevo = Exprevo(root)
exprevo.grid(padx=10,pady=10)

tk.Grid.columnconfigure(root, index=0, weight=1)
tk.Grid.rowconfigure(root, index=0, weight=1)

root.mainloop()
