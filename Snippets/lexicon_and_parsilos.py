from token_types import *

class Lexer(object):

    def __init__(self, process=""):
        self.process = process
        self.current_index = -1
        self.current_token = Token(BOF, None)
        self.current_char = None
        self._get_next_char()

    def _get_next_char(self):
        self.current_index += 1

        if self.current_index > len(self.process) - 1:
            # If there's no more input, return a empty string to signify
            next_char = ''
        else:
            # If we still have input to process, increment the character
            next_char = self.process[self.current_index]
        self.current_char = next_char

    def _get_next_token(self):
        # Stores the string value of the next token
        value = ''

        # Skip whitespace
        while self.current_char.isspace() or self.current_char == "\n":
            self._get_next_char()

        # Collect integers
        if self.current_char.isdigit() or self.current_char == "-":
            while self.current_char.isdigit() or self.current_char == "-":
                value += self.current_char
                self._get_next_char()
            return Token(INT, value)

        # Collect Strings
        if self.current_char == '"':
            self._get_next_char() # Advance past the first quotation
            while self.current_char != '"':
                if self.current_char == '':
                    return Token(ERR, "End of file reached during a string, check your quotes")
                value += self.current_char
                self._get_next_char()
            self._get_next_char() # Advance past the last quotation
            return Token(STR, value)

        if self.current_char == ",":
            self._get_next_char()
            return Token(SEP, COMMA)

        # Everything not already caught is qualified as a command
        # and checked to not be a boolean
        if self.current_char.isalpha():
            while self.current_char.isalpha() or self.current_char == "_":
                value += self.current_char
                self._get_next_char()
            if value == "true":
                return Token(BOOL, TRUE)
            if value == "false":
                return Token(BOOL, FALSE)
            return Token(COMMAND, value)

        # Checks to see if _get_next_char ever returned a empty string
        if self.current_char == '':
            return Token(EOF, None)
        else:
            # If something passed all of the checks, there's a problem
            return Token(ERR, f"unrecognized character: {self.current_char} @{self.current_index} | context: '{self.process[self.current_index-5:self.current_index+5]}'")

    def tokenize(self):
        tokens = []
        # Stops when it hits the end of file, or encounters an error
        while self.current_token.type != EOF:
            self.current_token = self._get_next_token()
            tokens.append(self.current_token)
            if self.current_token.type == ERR:
                print(f"Error: {self.current_token.value}")
                return None
        return tokens

# Parser
class Parser(object):

    def __init__(self, token_list, command_table, shortcut_table=None):
        # Contains the command names, arguments, and function counterparts of all the valid commands
        self.command_table = command_table
        self.shortcut_table = {} if shortcut_table is None else shortcut_table
        self.token_list = token_list
        self.current_index = -1
        self.current_token = Token(BOF, None)

    def _next_token(self):
        self.current_index += 1

        next_token = None

        # If there are no more tokens
        if self.current_index > len(self.token_list) - 1:
            next_token = Token(EOF, None)
        else:
            next_token = self.token_list[self.current_index]

        self.current_token = next_token

    def _last_token(self):
        self.current_index -= 1

        next_token = None

        # If we're at the start
        if self.current_index < 0:
            next_token = Token(BOF, None)
        else:
            next_token = self.token_list[self.current_index]

        self.current_token = next_token

    def parse(self):
        self.current_index = -1

        # While we haven't reached the last token
        # _next_token will set as an EOF if there are none
        while self.current_token.type != EOF:

            # To account for the -1 and the possibility of an empty string,
            # initial index was set to -1 and is advanced to catch any EOF
            self._next_token()

            command_name = None
            # A list of arguments parsed after the command
            args = []
            if self.current_token.type == COMMAND:
                command_info = self.command_table.get(self.current_token.value, None)
                command_name = self.current_token.value

                if command_info is None:
                    # Get command info from the shortcut reference
                    if self.current_token.value not in self.shortcut_table:
                        return Token(ERR, f"command {self.current_token.value} does not exist")
                    command_info = self.command_table[self.shortcut_table[self.current_token.value]]

                # Fill out the arg list
                for arg_info in command_info["args"]:

                    self._next_token() # Skip past the command token or get next arg

                    # If we need to collect all the remaining arguments
                    if arg_info[0] == TRAIL:

                        if self.current_token.type == SEP: # Skip comma
                                self._next_token()

                        # While the type requested is equal to the current type
                        # Catch all the trailing values of the same trailing type
                        while (self.current_token.type == arg_info[1]):

                            # Add it to the args
                            real = self._get_real(self.current_token.type, self.current_token.value)
                            args.append(real)
                            self._next_token()

                            if self.current_token.type == SEP: # Skip comma
                                self._next_token()

                        self._last_token()
                        break
                    
                    if self.current_token.type == SEP: # Skip comma
                        self._next_token()
                    
                    # If disequal types
                    if self.current_token.type != arg_info[0]:

                        # If no default value
                        if arg_info[1] == None:

                            # Throw clashing types error
                            return Token(ERR, f"{self.current_token.type} did not match {arg_info[0]}")

                        # If we do have a default value
                        # Get its pythonic value and add it to args
                        real = self._get_real(arg_info[0],arg_info[1])
                        args.append(real)

                        # recede the token
                        self._last_token()

                        continue


                    # If the next argument type is equal to the requested type
                    # Get its pythonic value and add it to args
                    real = self._get_real(self.current_token.type, self.current_token.value)
                    args.append(real)

                # Get and run the command with collected arguments
                command_function = command_info["function"]
                alias = self.shortcut_table.get(command_name,"")
                # print(f"*****\n[{command_name}:{alias}] called with args: {args}\n")
                returned = command_function(*args)
                # print(f"\n[{command_name}] finished | returned: {returned}\n")

        return Token(FIN, None)

    def _get_real(self, type, value):
        if type == INT:
            return int(value)
        if type == BOOL:
            return True if value == "+" else False
        if type == STR:
            return value