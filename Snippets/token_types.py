# Argument Tokens
INT = "integer"
STR = "string"
BOOL = "boolean"
TRAIL = "trailing"
#Bool Values
TRUE = "true"
FALSE = "false"

# Command Token
COMMAND = "command"

# Separator Tokens
SEP = "separator"
# Separator values
COMMA = "comma"

# Terminal Token
EOF = "end_of_file"
BOF = "beginning_of_file"

# Util Tokens
ERR = "error"
FIN = "finished"
EXIT = "exiting parser"

# Token
class Token(object):

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return "("+str(self.type)+", "+str(self.value)+")"