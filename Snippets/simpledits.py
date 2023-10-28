import tkinter as tk

class Simpledits(tk.Frame):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.text_widget = tk.Text(self)

		self.grid_widgets()

	def grid_widgets(self):
		self.text_widget.grid(row=0, column=0)

def get_text(start_with=""):

	window = tk.Tk()
	text = tk.StringVar()

	text_editor = Simpledits(window)
	text_editor.text_widget.insert(0.0,start_with)
	text_editor.grid(row=0, column=0, padx=5, pady=5)


	def exit(*a):
		text.set(text_editor.text_widget.get(0.0, tk.END))
		window.destroy()

	window.bind("<Control-Return>", exit)
	window.mainloop()

	return text.get().strip()