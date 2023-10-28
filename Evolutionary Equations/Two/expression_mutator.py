import random
from .expression import Expression

class ExpressionMutator(object):
	"""Handles the mutation of Expression objects.

	Attributes:
		(OperationManager) opman - used to recall symbols and their
			argument information
	"""

	def __init__(self, opman, termination_chance=0.5,
					termination_increment=0.1):
		 # OperationManager
		self.opman = opman
		self.termination_chance = termination_chance
		self.termination_increment = termination_increment


	def choose_random_child(self, expression):
		"""Returns a random nested child Expression of "expression"."""
		children = expression.get_all_child_exprs()
		child = random.choice(children)

		return child


	def mutate(self, expr):
		"""Chooses an Expression in the expr tree and mutates it."""

		expression = self.choose_random_child(expr)
		# prevent invalid expression from worming their way into the system
		# causes all sorts of problems
		self.fix_args(expression)

		mutations = [1,2,3,4]
		mutation = random.choice(mutations)


		if mutation == 1:
			self.mutate_symbol(expression)

		elif mutation == 2:
			self.mutate_to_parent(expression)

		elif mutation == 3:
			self.mutate_encapsulate(expression)

		elif mutation == 4:
			self.mutate_link(expression)


		self.fix_args(expression)

		return expr


	def mutate_symbol(self, expr):
		"""changes the symbol to a new random symbol."""

		expr.symbol = self.opman.get_random(avoid=expr.symbol)
		return expr


	def mutate_to_parent(self, expr):
		"""if expr has a parent, the parent object will be consumed by expr."""

		if expr.has_args(): # need to check to do anything other than iterating
			arg = random.choice(expr.args)
			expr.symbol = arg.symbol
			expr.clear_args()
			arg.reparent_args(expr)
			arg.disconnect()


	def mutate_encapsulate(self, expr):
		"""expr will become encasulated by a new expression."""
		
		expr_copy = expr.clone()
		expr.symbol = self.opman.get_random(1,atleast_min=True)
		expr.clear_args()
		expr_copy.connect(expr)


	def mutate_link(self, expr):
		"""if expr has args, it will be joined with one by a new expression
			if it doesn't have args, it will join with a random expression."""
		
		expr_copy = expr.clone()
		expr.symbol = self.opman.get_random(2,atleast_min=True)

		jumping = None
		if len(expr.args) > 0:
			jumping = random.choice(expr.args)
		else:
			jumping = self.generate_random_exp(0.5)

		expr.clear_args()
		jumping = jumping.clone(expr)
		expr_copy.connect(expr)


	def generate_random_exp(self, termination_chance=None, termination_increment=None):
		"""Recursively builds an expression object until termination_chance 
		is signifigantly high disallowing for expressions with arguments."""

		termination_chance = self.termination_chance if termination_chance is None else termination_chance
		termination_increment = self.termination_increment if termination_increment is None else termination_increment

		symbol = self.opman.get_random()
		data = self.opman.get_info(symbol)

		args = []
		needed_args = random.randrange(data["min_args"],data["max_args"]+1)

		for arg in range(needed_args):

			if random.random() < termination_chance:
				terminator = self.opman.get_random(0,0)
				args.append(Expression(terminator))
			else:
				args.append(
					self.generate_random_exp(
						termination_chance+termination_increment, 
						termination_increment)
					)

		expr = Expression(symbol)
		for arg in args:
			arg.connect(expr)

		return expr


	def fix_args(self, expression):
		"""Assures the expression has a correct number of args filling in
		discrepancies with new random expressions."""

		symbol = expression.symbol
		data = self.opman.get_info(symbol)
		min_args = data["min_args"]
		max_args = data["max_args"]

		arg_count = len(expression.args)
		while arg_count < min_args:

			# add a random arg
			self.generate_random_exp().connect(expression)
			arg_count += 1

		if arg_count > max_args:

			# truncate arg list
			expression.args = expression.args[:max_args]
