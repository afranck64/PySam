#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      said
#
# Created:     23.06.2012
# Copyright:   (c) said 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

try:
    from tkinter import *
    from tkinter.ttk import *
    from tkinter import filedialog
except:
    from Tkinter import *
    from ttk import *
    import tkFileDialog as filedialog
import sys
from os import path

for i in ("../", "../..", "../../.."):
    sys.path.append(path.abspath(i))


#from Console import Console
from ColoredText import ColoredText
from GConsole import GConsole
from machines import *


_FILE_TYPES = [("Pysam files", "*.psm"), ("All files", "*.*")]

class Application():
    def __init__(self):
        self.root = Tk()
        self.root.title("Python's Assembler - PySam")
        self.frm = Frame(self.root)
        self.frm.pack(expand=YES, fill=BOTH)
        self.titlemap = {}
        self.pages = {}
        self.counter = 1
        self.notebook = Notebook(self.frm)
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.newFile)
        filemenu.add_command(label="Open", command=self.openFile)
        filemenu.add_command(label="Save", command=self.saveFile)
        filemenu.add_command(label="Close", command=self.closeFile)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit)
        self.menubar.add_cascade(label="File", menu=filemenu)
        editmenu = Menu(self.menubar, tearoff=0)
        editmenu.add_command(label="Copy", command=self.copy)
        editmenu.add_command(label="Cut", command=self.cut)
        editmenu.add_command(label="Paste", command=self.paste)
        self.menubar.add_cascade(label="Edit", menu=editmenu)
        runmenu = Menu(self.menubar, tearoff=0)
        runmenu.add_command(label="Run", command=self.run)
        runmenu.add_command(label="Check")
        self.menubar.add_cascade(label="Run", menu=runmenu)
        aboutmenu = Menu(self.menubar, tearoff=0)
        aboutmenu.add_command(label="Help")
        aboutmenu.add_command(label="About")
        self.menubar.add_cascade(label="About", menu=aboutmenu)
        self.notebook.pack(side=TOP, expand=YES, fill=BOTH)
        self.notebook.enable_traversal()
        self.addFile("samples/demo.psm")
        self.console = GConsole(self.frm)
        self.console.pack(side=LEFT, expand=YES, fill=X)
        self.error = GConsole(self.frm)
        #self.error.pack(side=RIGHT, expand=YES, fill=X)
        #self.notebook.add(cText, text="Demo-1")
        """
        cons = Console(self.root)
        cons.appendtext("Hello world")
        cons.appendtext("fuck you")
        cons.pack()
        self.notebook.add(cons, text="Output")
        self.addFile("demo.psm")
        """
        self.root.bind("<Control-R>", lambda x:self.run())
        self.openfiles = []

    def addFile(self, filename):
        title = path.split(filename)[1]
        self.titlemap[title] = filename
        ctext = ColoredText(self.root)
        f = open(filename, "r")
        txt = f.read()
        ctext.text.insert(END, txt)
        f.close()
        ctext.pack()
        self.pages[title] = ctext
        self.notebook.add(ctext, text=title)

    def newFile(self):
        filename = "unsaved document - " + str(self.counter)
        self.counter += 1
        ctext = ColoredText(self.root)
        ctext.pack()
        self.pages[filename] = ctext
        self.titlemap[filename] = None
        self.notebook.add(ctext, text=filename)

    def closeFile(self):
        if len(self.notebook.tabs())==1:
            self.root.destroy()
            self.root.quit()
        else:
            self.notebook.forget("current")

    def copy(self):
        self.getCurrent().copy(None)

    def paste(self):
        self.getCurrent().paste(None)

    def cut(self):
        self.getCurrent().paste(None)
        pass

    def delete(self):
        self.getCurrent().delete(None)

    def getCurrent(self):
        name = self.notebook.tab("current")["text"]
        return self.pages[name]

    def getCurrentFile(self):
        name = self.notebook.tab("current")["text"]
        if name in self.titlemap:
            return self.titlemap[name]
        else:
            return None

    def exit(self):
        self.root.destroy()
        self.root.quit()

    def openFile(self):
        filename = filedialog.askopenfilename(filetypes=_FILE_TYPES)
        if filename and not filename in self.titlemap:
            title = self.notebook.tab("current")["text"]
            if not title in self.titlemap:
                ctext = self.pages[title]
                ctext.text.delete("1.0", END)
                ctext.text.insert("1.0", open(filename, encoding="utf8").read())
                nTitle = path.split(filename)[1]
                self.pages.pop(title)
                self.titlemap.pop(title)
                self.pages[nTitle] = ctext
                self.titlemap[nTitle] = filename
                self.notebook.tab("current", text=nTitle)
            self.addFile(filename)

    def run(self):
        """@GUI loop the GUI and blablabla... help"""
        content = self.notebook.tab("current")
        ctext = self.pages[content["text"]]
        text = ctext.gettext()
        try:
            self.console.clear()
            self.console.text.delete("1.0", END)
            machine = Loader.getMachine(text, output=self.console.output,
                                                input=self.console.input)
            machine.loop()
        except PySamException as err:
            line = int(err.line.split()[-1])
            self.getCurrent().text.higlight(line)
            self.console.output(str(err))
        """
        except Exception as err:
            self.console.output(str(err.args))
        """


    def saveFile(self):
        title = self.notebook.tab("current")["text"]
        filename = ""
        changed = False
        if self.titlemap[title]:
            filename = self.titlemap[title]
        else:
            filename = filedialog.asksaveasfilename(filetypes=_FILE_TYPES)
            changed = True
        if filename:
            f = open(filename, "w", encoding="utf8")
            f.write(self.pages[title].gettext())
            if changed:
                ctext = self.pages[title]
                nTitle = path.split(filename)[1]
                self.pages.pop(title)
                self.titlemap.pop(title)
                self.pages[nTitle] = ctext
                self.titlemap[nTitle] = filename
                self.notebook.tab("current", text=nTitle)



    def mainloop(self, n=0):
        self.root.mainloop(n)

if __name__ == "__main__":
    app = Application()
    app.root.mainloop()
