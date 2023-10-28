class Expression(object):
	"""Manages a symbol and list of child expressions. Functions as a node
	like object; many connected nodes will form a tree-like structure.

	Attributes:
		(str) symbol - determines what this expression object is
			used to locate other information such as how many args to 
			include.
		(Expression) parent - the expression to which this object is a 
			child of. In a tree of Expression objects, only one will have
			a None type parent.
		(list) args - the children of the Expression and the arguments
			to the symbol; i.e. func(a,b)
	"""

	def __init__(self, symbol="", parent=None, args=None):
		self.symbol = symbol
		self.parent = parent
		self.args = []

		args = [] if args is None else args

		# connect each arguments parent value to this Expression
		# forming a tree.
		for arg in args:
			arg.connect(self)


	def __str__(self):
		"""Renders the expression tree in the format of symbol(args)
		where each arg is recursively rendered.
		"""
		if self.has_args():
			string = f"{self.symbol}("
			for arg in self.args[:-1]:
				string += str(arg)+","
			return string + str(self.args[-1]) + ")"
		else:
			return self.symbol


	def has_args(self):
		return len(self.args) > 0


	def has_parent(self):
		return (not self.parent == None)


	def connect(self, to):
		"""Disconnects from current place in tree and reconnects as an
		arg of a "to".
		"""
		self.disconnect()
		self.parent = to
		if to != None:
			to.args.append(self)
		return self


	def disconnect(self):
		"""Removes self as an arg of current parent becoming the head
		of a new tree.
		"""
		if self.parent != None:
			self.parent.remove_arg(self)
			self.parent = None
		return self


	def remove_arg(self, arg):
		"""Removes and disconnects specified arg from arg list."""
		if arg in self.args:
			self.args.remove(arg)
		return self


	def clear_args(self):
		"""Removes and disconnects all args from arg list."""
		for arg in self.args[::-1]:
			arg.disconnect()
		return self


	def reparent_args(self, to):
		"""Removes and disconnects all args from arg list connecting them
		to a new parent epxression.
		"""
		for arg in self.args[::-1]:
			arg.connect(to)
		return self


	def get_all_child_exprs(self):
		"""Recursively returns a list of all Expression objects below
		self in the tree.
		"""
		children = [self]

		for arg in self.args:
			children += arg.get_all_child_exprs()

		return children


	def clone(self, parent_to=None):
		"""Recursively duplicates all Expression objects below self in
		tree returning an identical unique Expression instance.
		"""
		parent_to = self.parent if parent_to == None else parent_to
		new_expression = Expression(self.symbol)
		new_expression.connect(parent_to)
		for arg in self.args:
			arg.clone().connect(new_expression)
		return new_expression


	def serialize(self):
		"""Formats into a list object for easy JSON serlalization."""
		if not self.has_args():
			return self.symbol
		return [self.symbol]+[arg.serialize() for arg in self.args]


	def deserialize(self, expr_list):
		"""Recursively builds an Expression object from "expr_list"."""
		if type(expr_list) == str:
			self.symbol = expr_list
			return

		self.symbol = expr_list[0]
		for arg in expr_list[1:]:
			expr = Expression()
			expr.deserialize(arg)
			expr.connect(self)