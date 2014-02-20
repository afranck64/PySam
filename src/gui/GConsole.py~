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
    from tkinter import simpledialog
except:
    from Tkinter import *



class GConsole(Frame):
    def __init__(self, master=None, *args, **kw):
        Frame.__init__(self, master, *args, **kw)
        #self.pack(expand=YES, fill=X)
        self.makewidgets()
        self.appendtext("hello world")
        self.appendtext("how are you today?")

    def makewidgets(self):
        sbar = Scrollbar(self)
        text = Text(self, relief=SUNKEN, bg="gray", height=7)
        text.focus_set()
        sbar.config(command=text.yview)
        text.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        text.pack(side=LEFT, expand=YES, fill=X)
        self.text = text
        self.text.config(state="disable")

    def settext(self, text='', file=None):
        return
        if file:
            text = open(file, 'r').read()
        self.text.delete('1.0', END)
        self.text.insert('1.0', text)
        self.text.mark_set(INSERT, '1.0')
        self.text.focus()

    def appendtext(self, text='', file=None):
        return
        if file:
            text = open(file, 'r').read()
        self.text.insert(END, text)
        self.text.mark_set(INSERT, '1.0')
        self.text.focus()

    def gettext(self):
        return self.text.get('1.0', END+'-1c')

    def output(self, text=None):
        self.text.config(state="normal")
        self.text.insert(END, text)
        self.text.insert(END, "\n")
        self.text.see(END)
        self.text.config(state="disable")

    def clear(self):
        self.text.delete("1.0", END)

    def input(self):
        value = None
        edited = False
        print "getting input!!"
        """
        self.text.config(state="normal")
        self.text.insert(END, ">>> ")
        start = self.text.index("current")
        def back(self, event=None):
            current = self.text.index("current")
            ln, col = current.split(".")
            col_s = start.split(".")[1]
            if int(col) < int(col_s):
                self.text.delete(current, END)

        def validate(self, event=None):
            current = self.text.index("current")
            value = self.text.get(start, current)
            edited = True
            self.text.insert(END, "\n")
            return value
        self.bind("<BackSpace>", back)
        self.text.config(state="disable")
        self.text.bin("<Return>", validate)
        return value
        """
        res = simpledialog.askinteger("Input", "Enter an integer!")
        return res
        
    def validate(self):
        pass

if __name__ == "__main__":
    root = Tk()
    app = GConsole()
    app.mainloop()