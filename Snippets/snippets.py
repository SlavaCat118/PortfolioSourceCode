import os
import os.path

import json

from datetime import datetime

from token_types import *
import lexicon_and_parsilos as lap

import simpledits

class Snippets(object):

    def __init__(self, bookmarks_path=None):
        self.bookmarks_path = os.path.join(os.getcwd(), "bookmarks.json")
        self.bookmarks = {}

        self._load_bookmarks(self.bookmarks_path)

    def help(self):
        names = []
        args = []
        descs = []
        for command, info in snippets_command_table.items():
            name = f"[{command}] "
            for shortcut, destination in snippets_shortcut_table.items():
                if destination == command:
                    name += f"({shortcut}) "
            names.append(name)
            arg = ""
            for arg_info in info["args"]:
                arg += f"({arg_info[0]}:{arg_info[1]})"
            args.append(arg)
            descs.append(info["description"]+'\n')

        longest = 0
        for name in names:
            if len(name) > longest:
                longest = len(name)
        for n, i in enumerate(names):
            names[n] += " "*(longest-len(i)) + "| "

        longest = 0
        for arg in args:
            if len(arg) > longest:
                longest = len(arg)
        for n, i in enumerate(args):
            args[n] += " "*(longest-len(i)) + "| "

        for n, i in enumerate(names):
            print("> "+i+args[n]+descs[n])

    # FILE FUNCTIONS

    def get_file(self, file_path):
        if not os.path.exists(file_path):
            return f"file path <{file_path}> does not exist"
        with open(file_path, "r") as f:
            return f.read()

    def create_files(self, *files):
        for file in files:
            if not os.path.exists(file):
                open(file, "x").close()
                print(f"Created file <{file}>")
                continue
            print(f"file <{file}> already exists")

    def delete_files(self, *files):
        for file in files:
            if not os.path.exists(file):
                print(f"file <{file}> did not exist")
                continue
            print(f"Contents of <{file}>:\n\t"+self.get_file(file).replace("\n","\n\t"))
            os.remove(file)
            print(f"file <{file}> removed")

    def rename_file(self, old_path, new_path):
        if not os.path.exists(old_path):
            print(f"file <{old_path}> did not exist")
            return
        if os.path.exists(new_path):
            print(f"file <{new_path}> already exists")
            return
        os.rename(old_path, new_path)
        print(f"file <{old_path}> renamed to <{new_path}>")

    def print_files(self, *files):
        for file in files:
            print(f"--<{file}>---\n{self.get_file(file)}\n--</{file}>---")

    def modify_file(self, file, create_nonexistent, append, prefix):
        if not os.path.exists(file):
            if not create_nonexistent:
                print(f"file <{file}> did not exist")
                return
            self.create_files(file)

        file_contents = ""
        with open(file, "r") as f:
            file_contents = f.read()

        if append:
            text = simpledits.get_text(start_with="")
            with open(file, "a") as f:
                f.write(prefix+text)
        else:
            text = simpledits.get_text(start_with=file_contents)
            with open(file, "w") as f:
                f.write(text)

    def edit_file(self, file, create_nonexistent):
        self.modify_file(file, create_nonexistent, False, "")

    def append_file(self, file, create_nonexistent, title):
        prefix = "\n\n"+title + " | " + datetime.now().strftime("%B/%d/%Y %H:%M:%S") + "\n"
        self.modify_file(file, create_nonexistent, True, prefix)

    # DIRECTORY FUNCTIONS

    def create_dirs(self, *dirs):
        for dir in dirs:
            if os.path.isdir(dir):
                print(f"directory <{dir}> already exists")
                continue
            os.mkdir(dir)

    def delete_dirs(self, *dirs):
        # For all of our given dirs
        for dir in dirs:
            # Put ourselves inside the directory
            self.advance_context(dir)
            # Get a list of everything in our current context
            for path in os.listdir(self.get_context()):
                # if it's another dir, recursion recursion
                if os.path.isdir(path):
                    self.delete_dirs(path)
                # Now that we're done deleting all nested directories
                # Delete all the files in the directory
                if os.path.isfile(path):
                    self.delete_files(path)
            # After the deletion process is complete
            # Remove ourselves from the directory
            self.recede_context()
            # Delete the directory from its level up
            os.rmdir(dir)

    def rename_dir(self, old_dir_name, new_dir_name):
        if not os.path.exists(old_dir_name):
            print(f"directory <{old_dir_name}> does not exist")
            return
        if os.path.exists(new_dir_name):
            print(f"directory <{new_dir_name}> already exists")
            return
        os.rename(old_dir_name, new_dir_name)

    def print_dirs(self, recursive, *dirs, _prefix="\t"):
        for dir in dirs:
            # Move inside the dir
            self.advance_context(dir, False)

            # Get the contents
            contents = os.listdir(self.get_context())
            # Extracts dirs from contents
            contained_dirs = [i for i in contents if os.path.isdir(i)]
            # Extracts files from contents
            contained_files = [i for i in contents if os.path.isfile(i)]

            # Display files
            for file in contained_files:
                print(_prefix+"file: "+file)

            # Display directories and check if recursion recursion
            for contained_dir in contained_dirs:
                print(_prefix+f"dir:  {contained_dir}")
                if recursive:
                    self.print_dirs(True, contained_dir, _prefix=_prefix+"\t")
            self.recede_context(False)

    # BOOKMARK FUNCTIONS

    def _save_bookmarks(self):
        with open(self.bookmarks_path, "w") as f:
            json.dump(self.bookmarks, f, indent=4)

    def _load_bookmarks(self, path):
        with open(path, "r") as f:
            self.bookmarks = json.load(f)

    def create_bookmark(self, name):
        if name in self.bookmarks:
            print(f"bookmark <{name}> already exists")
            return
        self.bookmarks[name] = self.get_context()
        print(f"created bookmark <{name}> at <{self.get_context()}>")
        self._save_bookmarks()

    def delete_bookmarks(self, *names):
        for name in names:
            if name not in self.bookmarks:
                print(f"bookmark <{name}> does not exist")
                return
            location = self.bookmarks.pop(name)
            print(f"bookmark <{name}> was removed with location <{location}>")
        self._save_bookmarks()

    def rename_bookmark(self, old_name, new_name):
        if old_name not in self.bookmarks:
            print(f"bookmark <{old_name}> does not exist")
            return
        if new_name in self.bookmarks:
            print(f"bookmark <{new_name}> already exitst")
            return
        self.bookmarks[new_name] = self.bookmarks.pop(old_name)
        print(f"bookmark <{old_name}> renamed to <{new_name}>")
        self._save_bookmarks()

    def edit_bookmark(self, name, location):
        if old_name not in self.bookmarks:
            print(f"bookmark <{old_name}> does not exist")
            return
        self.bookmarks[name] = location
        print(f"bookmark <{name}> set to location <{location}>")
        self._save_bookmarks()

    def print_bookmarks(self, *names):
        for name in names:
            if name not in self.bookmarks:
                print(f"bookmark <{name}> does not exist")
                continue
            print(f"{name} | {self.bookmarks[name]}")

    def list_bookmarks(self):
        self.print_bookmarks(*list(self.bookmarks.keys()))

    def goto_bookmark(self, name):
        if name not in self.bookmarks:
            print(f"bookmark <{name}> does not exist")
            return
        self.set_context(self.bookmarks[name])

    def set_bookmark(self, name):
        if name not in self.bookmarks:
            print(f"bookmark <{name}> does not exist")
            return
        self.bookmarks[name] = self.get_context()
        self._save_bookmarks()

    # CONTEXT FUNCTIONS

    def advance_context(self, dir, _tell_me=True):
        if not os.path.isdir(dir):
            print(f"<{dir}> is not a directory or does not exits")
            return
        # Append the new directory to the current working directory
        os.chdir(os.path.join(os.getcwd(), dir))
        if _tell_me:
            print(f"advanced context to <{self.get_context()}>")

    def recede_context(self, _tell_me=True):
        # Pop the last dir off of the current working directory
        os.chdir(os.path.split(os.getcwd())[0])
        if _tell_me:
            print(f"receded context to <{self.get_context()}>")

    def set_context(self, path, _tell_me=True):
        if not os.path.isdir(path):
            print(f"path <{path}> was not a dir")

        os.chdir(path)
        if _tell_me:
            print(f"set context to <{self.get_context()}>")

    def print_context(self):
        print(self.get_context())

    def get_context(self):
        return os.getcwd()

    def list_context(self):
        observing = self.get_context()
        self.recede_context(False)
        self.print_dirs(False, observing)
        self.advance_context(observing, False)

    def walk_context(self):
        observing = self.get_context()
        self.recede_context(False)
        self.print_dirs(True, observing)
        self.advance_context(observing, False)
        

snippets = Snippets()

snippets_command_table = {
    "help": {
        "args":[],
        "function":snippets.help,
        "description":"Get help"
    },
    # FILE MANAGMENT
    "create_files":{
        "args":[[TRAIL,STR]],
        "function":snippets.create_files,
        "description":"Given [names], creates files at context"
    },
    "delete_files":{
        "args":[[TRAIL,STR]],
        "function":snippets.delete_files,
        "description":"Given [names], deletes files from context and prints content"
    },
    "rename_file":{
        "args":[[STR,None],[STR,None]],
        "function":snippets.rename_file,
        "description":"Given a [old file] and [new name], will rename the old file"
    },
    "edit_file":{
        "args":[[STR,None],[BOOL,FALSE]],
        "function":snippets.edit_file,
        "description":"Given a [name] and whether to [create if nonexistent], will open a text editor to edit the file"
    },
    "append_file":{
        "args":[[STR,None],[BOOL,FALSE],[STR,"Unnamed Entry"]],
        "function":snippets.append_file,
        "description":"Given a [name], whether to [create if nonexistent], and an [entry title], will append a titled entry, gotten from a text editor, to the specified file"
    },
    "modify_file":{
        "args":[[STR,None],[BOOL,FALSE],[BOOL,FALSE],[STR,""]],
        "function":snippets.modify_file,
        "description":"Given a [name], whether to [create if nonexistent], whether to [append], and (optionally) the [entry name]. Essentially a multipurpose file tool that combines the functionality of edit_file and append_file"
    },
    "print_files":{
        "args":[[TRAIL,STR]],
        "function":snippets.print_files,
        "description":"Given a [name], prints the contents of that file"
    },
    # CONTEXT MANGMENT
    "advance_context":{
        "args":[[STR,None]],
        "function":snippets.advance_context,
        "description":"Given a [directory], will advance the working directory inside it"
    },
    "recede_context":{
        "args":[],
        "function":snippets.recede_context,
        "description":"Pops the last directory off of the working directory"
    },
    "print_context":{
        "args":[],
        "function":snippets.print_context,
        "description":"Prints the current working directory"
    },
    "list_context":{
        "args":[],
        "function":snippets.list_context,
        "description":"Prints out the contents of the working directory"
    },
    "walk_context":{
        "args":[],
        "function":snippets.walk_context,
        "description":"Recursively prints out the entirety of the working directory tree"
    },
    # DIRECTORY MANAGMENT
    "create_dirs":{
        "args":[[TRAIL,STR]],
        "function":snippets.create_dirs,
        "description":"Given [names], will create a new directory for each, skipping already existing"
    },
    "delete_dirs":{
        "args":[[TRAIL,STR]],
        "function":snippets.delete_dirs,
        "description":"Given [names], will delete each directory recursively and the contents of each deleted file"
    },
    "rename_dir":{
        "args":[[STR,None],[STR,None]],
        "function":snippets.rename_dir,
        "description":"Given a [old dir] and a [new name], will rename the dir with a new name"
    },
    "print_dirs":{
        "args":[[BOOL,False],[TRAIL,STR]],
        "function":snippets.print_dirs,
        "description":"Given whether to [print recursively] and a list of [dirs] to print, will print the contents of each dir"
    },
    # BOOKMARK MANAGEMTN
    "create_bookmark":{
        "args":[[STR,None]],
        "function":snippets.create_bookmark,
        "description":"Given a [name], will create a new bookmark located at current working directory"
    },
    "delete_bookmarks":{
        "args":[[TRAIL,STR]],
        "function":snippets.delete_bookmarks,
        "description":"Given a [name], will delete that bookmark"
    },
    "rename_bookmark":{
        "args":[[STR,None],[STR,None]],
        "function":snippets.rename_bookmark,
        "description":"Given an [old name] and a [new name], will rename the old bookmark with a new name, preserving the location"
    },
    "edit_bookmark":{
        "args":[[STR,None],[STR,None]],
        "function":snippets.edit_bookmark,
        "description":"Given a [name] and [new location], will change the location of the bookmark"
    },
    "print_bookmarks":{
        "args":[[TRAIL,STR]],
        "function":snippets.print_bookmarks,
        "description":"Given [names], will print the names and locations of each bookmark"
    },
    "list_bookmarks":{
        "args":[],
        "function":snippets.list_bookmarks,
        "description":"Prints the names and locations of each bookmark you have"
    },
    "goto_bookmark":{
        "args":[[STR,None]],
        "function":snippets.goto_bookmark,
        "description":"Given a [name], will set the current working directory to the bookmarks location"
    },
    "set_bookmark":{
        "args":[[STR,None]],
        "function":snippets.set_bookmark,
        "description":"Given a [name], the bookmarks location will be updated to the current working directory"
    }
}

snippets_shortcut_table = {
    "h":"help",
    # FILES
    "cf":"create_files",
    "df":"delete_files",
    "rf":"rename_file",
    "ef":"edit_file",
    "af":"append_file",
    "mf":"modify_file",
    "pf":"print_files",
    # CONTEXT
    "ac":"advance_context",
    "rc":"recede_context",
    "pc":"print_context",
    "lc":"list_context",
    "wc":"walk_context",
    # DIRECTORIES
    "cd":"create_dirs",
    "dd":"delete_dirs",
    "rd":"rename_dir",
    "pd":"print_dirs",
    # BOOKMARKS
    "cb":"create_bookmark",
    "db":"delete_bookmarks",
    "rb":"rename_bookmark",
    "eb":"edit_bookmark",
    "pb":"print_bookmarks",
    "lb":"list_bookmarks",
    "gb":"goto_bookmark",
    "sb":"set_bookmark"
}

tokens = lap.Lexer('lc').tokenize()
if tokens != None:
    lap.Parser(tokens, snippets_command_table, snippets_shortcut_table).parse()

input_process = ""
return_token = Token(None, None)
while True:
    input_process = input(f"{os.path.basename(snippets.get_context())}>")
    tokens = lap.Lexer(input_process).tokenize()
    parser = lap.Parser(tokens, snippets_command_table, snippets_shortcut_table).parse()
    if parser.type == ERR:
        print(parser)   