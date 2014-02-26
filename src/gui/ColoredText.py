#!/usr/bin/env python

try:
    from tkinter import *
    from tkinter.ttk import *
    #from tkinter import filedialog
except:
    from Tkinter import *

from idlelib.Percolator import Percolator

import time
import re
import keyword
#import builtins
#from tkinter import *
from idlelib.Delegator import Delegator
from idlelib.configHandler import idleConf


from ColorDelegator import ColorDelegator

DEBUG = False

BUILTIN = ["swap", "load", "store", "push", "pop", "copy",
                   "add", "sub", "mul", "div", "mod", "sqrt", "pow",]
KEYWORD = ["jez", "jgz", "jlz", "jge", "jle", "goto", "output",
                        "val", "input"]

class Text2(Text):
    def __init__(self, master, **kw):
        Text.__init__(self, master, **kw)
        self.bind('<Control-c>', self.copy)
        self.bind('<Control-x>', self.cut)
        self.bind('<Control-v>', self.paste)
        self.bind("<Control-u>", self.selectall)
        self.bind("<KeyPress>", self.dellight)

    def selectall(self, event=None):
        event.widget.tag_add("sel","1.0","end")

    def copy(self, event=None):
        self.clipboard_clear()
        text = self.get("sel.first", "sel.last")
        self.clipboard_append(text)

    def cut(self, event=None):
        self.copy()
        self.delete("sel.first", "sel.last")

    def paste(self, event=None):
        text = self.selection_get(selection='CLIPBOARD')
        self.insert('insert', text)

    def higlight(self, line):
        start = "%s.0" % (line)
        end = "%s.0" % (line + 1)
        self.tag_configure("highlight", background="bisque")
        self.tag_add("highlight", start, end)
        self.see(start)

    def dellight(self, event=None):
        self.tag_delete("highlight")



class ColoredText(Frame):

    def __init__(self, parent=None, text='', file=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)
        self.makewidgets()


    def makewidgets(self):
        sbar = Scrollbar(self)
        text = Text2(self, relief=SUNKEN)
        text.focus_set()
        p = Percolator(text)
        d = ColorDelegator()
        p.insertfilter(d)
        sbar.config(command=text.yview)
        text.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        text.pack(side=LEFT, expand=YES, fill=BOTH)
        self.text = text
        self.copy = text.copy
        self.paste = text.paste
        self.delete = text.delete
        self.cut = text.cut
        self.highlight = text.higlight


    def settext(self, text='', file=None):
        return
        if file:
            text = open(file, 'r').read()
        self.text.insert('1.0', text)
        self.text.mark_set(INSERT, '1.0')
        self.text.focus()

    def gettext(self):
        return self.text.get('1.0', END+'-1c')

def main():
    from idlelib.Percolator import Percolator
    root = Tk()
    #root.wm_protocol("WM_DELETE_WINDOW", root.quit)
    text = ColoredText(root)
    root.mainloop()

if __name__ == "__main__":
    main()