import os, os.path, pyperclip, tkinter as tk, shutil
from datetime import datetime
import json

class Snippets(object):
    """docstring for Snippets"""

    def __init__(self, context = "snippets/", *args, **kwargs):
        self.context = context
        self.helpScreen =       """

        Welcome to Snippets

        COMMANDS:
        - ac file/dir ) Advances file context by file/dir
        - rc          ) Recedes file context by one
        - pc          ) Prints currents context
        - lc          ) Lists current context
        - wc          ) Walks through every file in context
        - pf file     ) Prints contents of context + file
        - cf file     ) Copies contents of context + file to clipboard
        - wf file     ) Writes gotten text to file
        - ef fo;e     ) Edits the contents of the file
        - df *files   ) Deletes context + *files
        - mf *files   ) Makes a file
        - rf file     ) Renames file to text
        - p           ) Prints context if file
        - c           ) Copies context if file
        - w           ) Writes gotten text to context if file
        - e           ) Edits the context if file
        - d           ) Deletes context file and recedes
        - r           ) Renames context
        - md *dirs    ) Adds *dirs to context
        - dd *dirs    ) Deletes *dirs
        - lb          ) See all available bookmarks
        - mb          ) Create a bookmark
        - db name     ) Delete bookmark at index
        - gb name     ) Goto bookmark at index
        - h           ) See this
                """

        with open("bookmarks.json", "r") as f:
            self.bookmarks = json.load(f)

    def getPath(self, file = ""):
        if os.path.isdir(self.context):
            path = os.path.join(self.context, file)
        else:
            path = self.context
        path = os.path.normpath(path)
        return path

    def listBookmarks(self):
        for k, v in self.bookmarks.items():
            print(k + ": " + v)

    def gotoBookmark(self, name):
        self.setContext(self.bookmarks[name])

    def createBookmark(self, name):
        self.bookmarks[name] = self.context
        self.saveBookmarks()

    def saveBookmarks(self):
        with open("bookmarks.json", "w") as f:
            f.write(json.dumps(self.bookmarks, indent = 4))

    def deleteBookmark(self, name):
        self.bookmarks.pop(name)
        self.saveBookmarks()

    def advanceContext(self, newContext):
        advanced = os.path.join(self.context, newContext)
        if os.path.exists(advanced):
            self.context = advanced
            print(f"context: {self.context}")
        else:
            print("advance failed, not a file or dir")
        return self.context

    def recedeContext(self):
        self.context = os.path.split(self.context)[0]
        print(f"context: {self.context}")

    def listContext(self):
        if os.path.isdir(self.context):
            print(os.listdir(self.context))

    def setContext(self, path):
        if os.path.exists(path):
            self.context = path

    def walkContext(self):
        if os.path.isdir(self.context):
            for i in os.walk(self.context):
                if len(i[2]) > 0:
                    print(os.path.normpath(os.path.join(i[0], i[2][0])))
                else:
                    print(f"{os.path.normpath(i[0])} empty")

    def openFile(self, file = "", tag = "r"):
        path = self.getPath(file)
        if os.path.isfile(path):
            return open(path, tag)
        else:
            print("context not file")
            return None

    def writeFile(self, file = "", title = "", text = ""):
        path = self.getPath(file)
        with open(path, "a") as f:
            data = datetime.now()
            data = data.strftime("%B/%d/%Y %H:%M:%S")
            f.write(title + " | "+ data + "\n" + text + "\n")
        print(f"Appended text to {path}")

    def editFile(self, file="", text=""):
            path = self.getPath(file)
            with open(path, "w") as f:
                f.write(text)

    def printFile(self, file = ""):
        got = self.openFile(file)
        if got != None:
            print("---< "+file+" >---")
            print(got.read() + "---</ "+file+" >---\n")
            got.close()

    def copyFile(self, file = ""):
        got = self.openFile(file)
        if got != None:
            pyperclip.copy(got.read())
            got.close()
            print(f"copied file")

    def deleteFile(self, file = ""):
        path = self.getPath(file)
        if os.path.isfile(path):
            confirm = input("are you sure y/n")
            if confirm.lower() == 'y':
                os.remove(path)
                print(f"removed {path}")
            else:
                print("deletion aborted")
        else:
            print("not a file")

    def makeFile(self, *files):
        if os.path.isfile(self.context):
            print("please recede context to a directory")
            return

        for i in files:
            path = os.path.normpath(os.path.join(self.context, i))
            f = open(path, "x")


    def addDirs(self, *dirs):
        for i in dirs:
            path = os.path.normpath(os.path.join(self.context, i))
            if not os.path.isdir(os.path.normpath(os.path.join(self.context, i))):
                os.mkdir(path)
                print(f"made dir {path}")
            else:
                print(f"dir {i} already exists in {path}")

    def deleteDir(self, *dirs):
        for i in dirs:
            path = os.path.normpath(os.path.join(self.context, i))
            if os.path.isdir(path):
                confirm = input("are you sure y/n")
                if confirm.lower() == 'y':
                    shutil.rmtree(path)
                    print(f"deleted {path}")
                else:
                    print("deletion aborted")
            else:
                print(f"{i} not a dir in {path}")

    def renameDir(self, dir_, name):
        path = os.path.join(self.context, dir_)
        if os.path.isdir(path):
            os.rename(path, os.path.join(self.context, name))
            print(f"{path} renamed to {name}")

    def help(self):
        print(self.helpScreen)


def multitext(init_text=""):

    print("Press Ctrl+Enter to return")

    global retText
    root = tk.Tk()
    text = tk.Text(root, width = 100, height = 20)
    text.grid(sticky = tk.NSEW, padx = 5, pady = 5)

    text.insert(0.0,init_text)

    text.focus_set()

    def onClose(*a):
        global retText
        retText = text.get(0.0, tk.END)
        root.destroy()

    text.bind("<Control-Return>", onClose)

    root.protocol("WM_DELETE_WINDOW", onClose)
    root.focus_force()
    root.mainloop()

    return retText

def parseCommand(command):
    commands = list()
    word = ""
    for i in command:
        if i != " ":
            word += i
        else:
            if word != "":
                commands.append(word.strip())
                word = ""
    if word != "":
        commands.append(word.strip())
    return commands

def processCommands(snippets, commands):

    advancingContext = False
    writingFile = False
    editingFile = False
    printingFile = False
    copyingFile = False
    addingDirs = False
    deletingFile = False
    deletingDirs = False
    renamingDir = False
    makingFile = False
    creatingBookmark = False
    deletingBookmark = False
    gotoBookmark = False

    renameDir = ""

    for n, i in enumerate(commands):
        if i == "ac":
            advancingContext = True
        elif i == "pf":
            printingFile = True
        elif i == "cf":
            copyingFile = True
        elif i == "wf":
            writingFile = True
        elif i == "ef":
            editingFile = True
        elif i == "md":
            addingDirs = True
        elif i == "df":
            deletingFile = True
        elif i == "dd":
            deletingDirs = True
        elif i == "mf":
            makingFile = True
        elif i == "rc":
            snippets.recedeContext()
        elif i == "lc":
            snippets.listContext()
        elif i == "wc":
            snippets.walkContext()
        elif i == "pc":
            print(snippets.context)
        elif i == "c":
            snippets.copyFile()
        elif i == "p":
            snippets.printFile()
        elif i == "w":
            title = input("title: ")
            snippets.writeFile(title=title.strip(), text = multitext())
        elif i == "e":
            snippets.editFile(file=snippets.context, text=multitext(snippets.openFile(snippets.context).read()))
        elif i == "d":
            snippets.deleteFile()
            snippets.recedeContext()
        elif i == "lb":
            snippets.listBookmarks()
        elif i == "db":
            deletingBookmark = True
        elif i == "gb":
            gotoBookmark = True
        elif i == "mb":
            creatingBookmark = True
        elif i == "h" or i == "help":
            snippets.help()
        else:
            if advancingContext:
                snippets.advanceContext(i)
            elif printingFile:
                snippets.printFile(i)
            elif copyingFile:
                snippets.copyFile(i)
            elif writingFile:
                title = input("title: ")
                text = multitext()
                snippets.writeFile(i, title.strip(), text.strip())
            elif addingDirs:
                snippets.addDirs(i)
            elif deletingFile:
                snippets.deleteFile(i)
            elif deletingDirs:
                snippets.deleteDir(i)
            elif makingFile:
                snippets.makeFile(i)
            elif deletingBookmark:
                snippets.deleteBookmark(i)
            elif gotoBookmark:
                snippets.gotoBookmark(i)
            elif creatingBookmark:
                snippets.createBookmark(i)
            elif editingFile:
                snippets.editFile(i, multitext(snippets.openFile(i).read()))
            elif renamingDir:
                if renamingDir == "":
                    renameDir = i
                else:
                    snippets.renameDir(renameDir, i)

def main(*args):
    snippets = Snippets()
    snippets.help()
    command = ""
    print(

        )
    while command != "quit":
        command = input(snippets.context + "> ")
        commands = parseCommand(command)
        processCommands(snippets, commands)

main()
