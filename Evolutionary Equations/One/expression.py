import random
import os

from allowed_operators import FUNCTIONS, OPERATORS, STOPS, VARNAMES

FULL = FUNCTIONS | {i:2 for i in OPERATORS}

class Expression(object):
	"""docstring for Expression"""

	def __init__(self, operator=None, args=None):
		self.operator = operator
		self.args = list() if args is None else args

		# adds readability to the output expression, not valid GMIC (unless
		# "")
		self.spacing = ""

		# list of var names the var operator can pull from
		self.var_names = VARNAMES

	def __str__(self):
		# if we have a function
		if self.operator in FUNCTIONS:
			# string its name and args in func notation: sin(x)

			base_string = self.operator+"(" + self.spacing
			for n, arg in enumerate(self.args):
				base_string += str(arg)
				# put commas after each argument except the last
				if n != len(self.args)-1:
					base_string += "," + self.spacing

			return base_string + self.spacing + ")"

		# if we have an operator
		elif self.operator in OPERATORS:
			# string its two argument to each side of the operator
			return "("+str(self.args[0]) +self.spacing + self.operator + self.spacing + str(self.args[1])+")"

		# if we have a stopper
		else:
			return self.operator

	def generate_expression(self):
		operator = None
		needed_args = 0
		args = list()

		# determine a random operator
		# 60% chance to get a function
		if random.random() < 0.6:
			# Even distribution between operators and functions, although
			# the only difference between them is visual
			if random.random() < 0.5:
				# operator is a random function
				operator = random.choice(list(FUNCTIONS.keys()))
			else:
				# operator is a random operator
				operator = random.choice(OPERATORS)
		else:
			# operator is a random variable or const
			# stops act as a recursion ending condition as they have no
			# arguments, needed to keep equations within recursion depth
			# limits.
			operator = random.choice(STOPS)

		# generate the desired amount of arguments
		if operator not in STOPS:
			if operator in FUNCTIONS:

				# functions define the amount of arguments they need
				needed_args = FUNCTIONS[operator]
				if needed_args == -1:
					# -1 == function can take an unlimited amount of args
					# limited to at most three for size reasons, can be
					# later mutated to have more
					needed_args = random.randrange(1,3)
				elif needed_args < -1:
					# anything less than -1 means that the func can take
					# up to the abs(needed_args) args
					needed_args = random.randrange(1,-needed_args)
			elif operator in OPERATORS:
				# operators can only have two args (arg) + (arg)
				needed_args = 2

			# generate a new expression for each argument
			for i in range(needed_args):
				arg = Expression()
				arg.generate_expression()
				args.append(arg)
		else:
			# the following do not take expressions as arguments
			if operator == "var":
				operator = random.choice(self.var_names)
			elif operator == "num":
				operator = str(random.randrange(-100,100))

		self.operator = operator
		self.args = args

	def get_all_child_expressions(self):
		child_expressions = [self]
		for arg in self.args:
			child_expressions += arg.get_all_child_expressions()
		return child_expressions

	def mutate(self, num=1):
		mutation_type = random.randrange(0,5)
		children = self.get_all_child_expressions()
		mutating = random.choice(children)

		if mutation_type == 0:
			mutating.mutate_expression()
		if mutation_type == 1:
			mutating.mutate_adjust()
		if mutation_type == 2:
			mutating.mutate_lower()
		if mutation_type == 3:
			mutating.mutate_raise()
		if mutation_type == 4:
			mutating.mutate_jump()

	def mutate_expression(self):
		if len(self.args) > 0:
			for arg in self.args:
				arg.generate_expression()
		else:
			self.generate_expression()

	def mutate_adjust(self):
		# If we don't have a var or val
		if len(self.args) > 0:
			# pick a new operator from both funcs and opers
			self.operator = random.choice(list(FULL.keys()))
			needed_args = FULL[self.operator]

			# account for nonstandard needed_args
			if needed_args == -1:
				needed_args = random.randrange(1,3)
			elif needed_args < -1:
				needed_args = random.randrange(1,-needed_args)

			# force compatibility:
			while len(self.args) < needed_args:
				new_arg = Expression()
				new_arg.generate_expression()
				self.args.append(new_arg)
			while len(self.args) > needed_args:
				self.args.pop()
		else:
			if self.operator.isdigit():
				self.operator = str(int(self.operator) + random.uniform(-10,10))
			else:
				self.operator = random.choice(self.var_names)

	def mutate_lower(self):
		# preserve current state
		self_copy = self.copy()

		# get new operator
		self.mutate_adjust()

		if len(self.args) > 0:
			self.args[0] = self_copy

	def mutate_raise(self):
		if len(self.args) > 0:
			chosen_arg = random.choice(self.args)
			self.operator = chosen_arg.operator
			self.args = chosen_arg.args

	def mutate_jump(self):
		if len(self.args) > 0:
			new_operator = random.choice(OPERATORS)

			self_copy = self.copy()
			jumping = random.choice(self.args)

			self.operator = new_operator
			self.args = [self_copy,jumping]

	def to_json(self):
		return [
			self.operator,
			[arg.to_json() for arg in self.args]
		]

	def from_json(self, expression):
		self.operator = expression[0]
		self.args = []
		for arg in expression[1]:
			new_arg = Expression()
			new_arg.from_json(arg)
			self.args.append(new_arg)

	def copy(self):
		new_args = []
		for arg in self.args:
			new_args.append(arg.copy())
		return Expression(self.operator, new_args)

	def render_to(self, dir, num=0, width=200,height=200):
		os.system(f"gmic {width},{height},1,1,\"{str(self)}\" n 0,255 o {dir}/exprevo_output_cache_{num}.png")
		return f"{dir}/exprevo_output_cache_{num}.png"

	def get_gmic_function(self, width, height):
		return f"gmic {width},{height},1,1,\""+str(self)+"\""

# test = Expression("sinc",
# 		[Expression("rol",
# 			[Expression("&",
# 				[Expression("y"),
# 				Expression("+",
# 						[Expression("x"),
# 						Expression("&",
# 								[Expression("y"),
# 								Expression("fibo",
# 										[Expression("*",
# 											[Expression("0.1"),
# 											Expression("-",
# 												[Expression("x"),
# 												Expression("-",
# 													[Expression("y"),
# 													Expression("100")
# 													]
# 													)
# 												]
# 												)
# 											]
# 											)
# 										]
# 									)
# 								]
# 							)
# 						]
# 					)]
# 				)
# 			])
# 		]
# 	)

# print(test.get_gmic_function(200,200))
# for i in range(20):
# 	test.mutate()
# print(test)
# test.render_to("image_cache",0)