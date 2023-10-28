from .operator_manager import FUNCTION, OPERATOR, VARIABLE, DECORATOR

class Compiler:
	"""Returns an expression object in string format for use in another
	program. compiler attribute is a function used to render the expression"""

	def __init__(self, opman):
		self.opman = opman

	def compile(self, *exprs):
		compilations = []
		for expr in exprs:
			compilations.append(str(expr))
		return compilations


class GmicCompiler(Compiler):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)


	def compile(self, *expressions):

		def render_expression(expr):
			style = self.opman.get_info(expr.symbol)["render_style"]
			if style == FUNCTION:
				string = f"{expr.symbol}("

				for n,i in enumerate(expr.args):
					string += render_expression(i)
					if n < len(expr.args)-1:
						string += ","

				return string + ")"

			if style == OPERATOR:
				left = render_expression(expr.args[0])
				right = render_expression(expr.args[1])
				return "(" + left + expr.symbol + right + ")"

			if style == VARIABLE:
				return expr.symbol

			if style == DECORATOR:
				return "(" + expr.symbol + render_expression(expr.args[0]) + ")"

		compiled_string = "\""

		if len(expressions) < 2:
			return compiled_string + render_expression(expressions[0]) + "\""

		compiled_string += "["
		for n, expr in enumerate(expressions):
			compiled_string += render_expression(expr)

			if n < len(expressions)-1:
				compiled_string += ","

		return compiled_string + "]\""