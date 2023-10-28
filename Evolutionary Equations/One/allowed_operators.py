# -1 = atleast one
# <-1 = at most n args (-2 = at most 2 args (atleast one))

# custom test sets
"""
FUNCTIONS = {
	"sin":1,
	"cos":1,
	"tan":1
}
STOPS = [
	"var",
	"num",
]
VARNAMES = ["x","y"]
OPERATORS = [
	"+",
	"-",
	"*",
	"/",
	"^"
]"""

# FUNCTIONS = {
# 	"sin":1,
# 	"cos":1
# }
# STOPS = [
# 	"var",
# 	"num",
# ]
# VARNAMES = ["x","y","x","y","pi"]
# OPERATORS = [
# 	"-",
# 	"+",
# 	"*",
# 	"/",
# 	"^",
# ]

## ideal test set
FUNCTIONS = {
    "abs":1, 
    "acos":1, 
    "asin":1, 
    "asinh":1, 
    "atan":1, 
    "atan2":2, 
    "atanh":1, 
    "avg":-1, 
    "bool":1, 
    "cbrt":1, 
    "ceil":1, 
    "cos":1, 
    "cosh":1, 
    "cut":3, 
    "deg2rad":1, 
    "erf":1, 
    "erfinv":1, 
    "exp":1, 
    "fact":1, 
    "fibo":1, 
    "floor":1, 
    "gamma":1, 
    "gauss":1, 
    "gcd":2, 
    "int":1, 
    "log":1, 
    "log2":1, 
    "log10":1, 
    "med":-1, 
    "prod":-1, 
    "rad2deg":1, 
    "rol":-2, 
    "ror":-2, 
    "round":-3, 
    "sign":1, 
    "sin":1, 
    "sinc":1, 
    "sinh":1, 
    "sqrt":1, 
    "sum":-1, 
    "tan":1, 
    "tanh":1, 
    "xor":2,
}
VARNAMES = ["x","y","x","y","x","y","e","pi","u","v","g"]
STOPS = [
    "var",
    "num",
]
OPERATORS = [
    "||",
    "&&",
    "|",
    "&",
    "!=",
    "==",
    "<=",
    ">=",
    "<",
    ">",
    "-",
    "+",
    "*",
    "/",
    "^",
]

# Complete test set
# FUNCTIONS = {
# 	"abs":1, 
# 	"acos":1, 
# 	"asin":1, 
# 	"asinh":1, 
# 	"atan":1, 
# 	"atan2":2, 
# 	"atanh":1, 
# 	"avg":-1, 
# 	"bool":1, 
# 	"cbrt":1, 
# 	"ceil":1, 
# 	"cos":1, 
# 	"cosh":1, 
# 	"cut":3, 
# 	"deg2rad":1, 
# 	"erf":1, 
# 	"erfinv":1, 
# 	"exp":1, 
# 	"fact":1, 
# 	"fibo":1, 
# 	"floor":1, 
# 	"gamma":1, 
# 	"gauss":1, 
# 	"gcd":2, 
# 	"int":1, 
# 	"isnan":1, 
# 	"isnum":1, 
# 	"isinf":1, 
# 	"isint":1, 
# 	"isbool":1, 
# 	"isin":1, 
# 	"log":1, 
# 	"log2":1, 
# 	"log10":1, 
# 	"max":1, 
# 	"maxabs":1, 
# 	"med":-1, 
# 	"min":1, 
# 	"minabs":1, 
# 	"prod":-1, 
# 	"rad2deg":1, 
# 	"rol":-2, 
# 	"ror":-2, 
# 	"round":-3, 
# 	"sign":1, 
# 	"sin":1, 
# 	"sinc":1, 
# 	"sinh":1, 
# 	"sqrt":1, 
# 	"sum":-1, 
# 	"tan":1, 
# 	"tanh":1, 
# 	"xor":2,
# }
# VARNAMES = ["x","y","x","y","x","y","e","pi","u","v","g"]
# STOPS = [
# 	"var",
# 	"num",
# 	"const"
# ]
# OPERATORS = [
# 	"||",
# 	"&&",
# 	"|",
# 	"&",
# 	"!=",
# 	"==",
# 	"<=",
# 	">=",
# 	"<",
# 	">",
# 	"-",
# 	"+",
# 	"*",
# 	"/",
# 	"^",
# ]

# This is just a smaller test set
"""FUNCTIONS = {
	"abs":1, 
	"acos":1, 
	"asin":1, 
	"atan":1, 
	"avg":-1, 
	"cos":1, 
	"cut":3, 
	"deg2rad":1, 
	"fact":1, 
	"floor":1, 
	"gauss":1, 
	"gcd":2, 
	"log":1, 
	"max":-1, 
	"min":-1, 
	"rad2deg":1, 
	"round":-3, 
	"sign":1, 
	"sin":1, 
	"sqrt":1, 
	"tan":1, 
	"xor":2,
}
# VARNAMES = ["x","y","x","y","x","y","e","pi","u","v","g"]
STOPS = [
	"var",
	""
]
OPERATORS = [
	"||",
	"&&",
	"!=",
	"==",
	"<=",
	">=",
	"<",
	">",
	"-",
	"+",
	"*",
	"/",
	"%",
	"^",
]"""
