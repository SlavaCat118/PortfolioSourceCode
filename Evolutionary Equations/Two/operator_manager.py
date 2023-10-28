import random
import json


FUNCTION = 0  # FUNCTION(arg)    | sin(x)
OPERATOR = 1  # arg OPERATOR arg | (1 + 10)
VARIABLE = 2  # VARIABLE         | y
DECORATOR = 3 # DECORATOR arg    | (!10)

style_names = ["FUNCTION","OPERATOR","VARIABLE","DECORATOR"]

class OperatorManager(object):
	"""Handles the information, useability, and selection of operators."""
	

	def __init__(self, operators=None, active=None, num_range=(-100,100), 
					num_chance=0.3, print_guesses=False):

		self.operators = operators if operators is not None else dict()
		"""
		self.operators[symbol] = {
			"min_args":min_args,
			"max_args":max_args,
			"render_style":render_style,
			"chance":chance
		}
		"""
		self.active = active if active is not None else []

		self.num_range = num_range
		self.num_chance = num_chance
		self.num_info = {
			"min_args":0,
			"max_args":0,
			"render_style": VARIABLE
		}

		self.print_guesses = print_guesses


	def __str__(self):
		string = "\n"
		for symbol, info in self.operators.items():
			style = style_names[info["render_style"]]
			string += f"{symbol}: {style} | {info['min_args']}-{info['max_args']} args | {info['chance']}%\n"
		return string


	def get_info(self, symbol):
		"""Returns operator information for the given symbol."""
		if symbol not in self.operators.keys():

			if symbol.removeprefix("-").isdigit():
				return self.num_info

			raise KeyError(f"Symbol \"{symbol}\" was not found")

		return self.operators.get(symbol)


	def add(self, symbol, min_args=0, max_args=None, chance=100, render_style=None, activate=True):
		"""Adds a new operator to the 'operators'."""
		max_args = min_args if max_args is None else max_args

		if render_style == None:
			if max_args == 0:
				render_style = VARIABLE
			elif not symbol.isalpha():
				if max_args == 2:
					render_style = OPERATOR
				else:
					render_style = DECORATOR
			else:
				render_style = FUNCTION

			if self.print_guesses:
				print(f"No render style provided for {symbol}, guessed: {style_names[render_style]}")

		if render_style == OPERATOR and not (min_args==2 and max_args==2):
			raise TypeError(f"{symbol} must have exactly two args to render as an operator")

		self.operators[symbol] = {
			"min_args":min_args,
			"max_args":max_args,
			"render_style":render_style,
			"chance":chance
		}

		if activate:
			self.activate(symbol)


	def remove(self, symbol):
		"""Removes symbol from 'operators'."""
		if symbol in self.operators:
			self.operators.remove(symbol)
			self.deactivate(symbol)


	def activate(self, symbol):
		"""Adds symbol to list of active operators."""
		self._append_unique(symbol, self.active)


	def deactivate(self, symbol):
		"""Removes symbol from list of active operators."""
		self.active.remove(symbol)


	def get_random_number(self):
		return str(random.randrange(*self.num_range))


	def get_random(self, min_args=None, max_args=None, atleast_min=False, atmost_max=False, avoid=None):
		"""Returns a random operator matching the requirements given."""
		avoid = [] if avoid is None else avoid
		available = [i for i in self.active if i not in avoid]

		valid = []

		for symbol in available:
			data = self.operators[symbol]

			op_min_args = data["min_args"]
			op_max_args = data["max_args"]
			chance = data["chance"]

			# if min_args <= symbol_args <= max_args

			# if operator matches in min_args or has a greater min_args
			if (min_args==None) or ((min_args == op_min_args) or 
				(atleast_min and min_args <= op_min_args)):


				# if the operator matches in max_args or has less max_args
				if (max_args==None) or ((max_args == op_max_args) or
					(atmost_max and max_args >= op_max_args)):

					valid += [symbol, chance]

		if len(valid) > 0:

			# If we don't want any arguments
			if max_args == 0 or (max_args == None and min_args == 0):

				# if we roll the chace to have a number
				if random.random() > self.num_chance:
					return self.get_random_number()

			return random.choices(
				population=valid[::2],
				weights=valid[1::2],
				k=1)[0]
		else:

			# If we don't want any arguments
			if max_args == 0 or (max_args == None and min_args == 0):
					return self.get_random_number()

		error_str = "no operators have "
		if atleast_min:
			error_str += "atleast "
		error_str += str(min_args) + " and "
		if atmost_max:
			error_str += "atmost "
		error_str += str(max_args) + " args"

		raise IndexError(error_str)


	def _append_unique(self, item, to):
		if item in to:
			return 
		to.append(item)


	def serialize(self):
		"""Returns a dict of all settings."""
		return {
			"operators":self.operators,
			"active":self.active,
			"num_range":self.num_range,
			"num_chance":self.num_chance,
		}


	def deserialize(self, settings):
		"""Sets values to given settings."""
		self.operators = settings["operators"]
		self.active = settings["active"]
		self.num_range = settings["num_range"]
		self.num_chance = settings["num_chance"]


	def load(self, path):
		with open(path, "r") as f:
			string = f.read()
			struct = json.loads(string)
			self.JSON_deserialize(struct)


# opman = OperatorManager()
# opman.add("1_arg",1)
# opman.add("2_arg",2)
# opman.add("1_to_2_args",1,2)
# opman.add("3_args",3)
# opman.add("0_arg",0)
# opman.add("0_to_10_arg",0,10)

# # 1 to 3 args
# print(opman.get_random(1,3,True,True))
# # atleast 2 args
# print(opman.get_random(2, atleast_min=True))
# # atleast 1 atmost 2
# print(opman.get_random(1,2,True,True))
# # 2 args
# print(opman.get_random(2))
# print(opman.get_random(0,0))
# print(opman.get_random(0,0))