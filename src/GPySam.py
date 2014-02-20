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

import sys
import os.path as path
sys.path.append(path.abspath(".\gui"))
sys.path.append(path.abspath(".\machines"))
import machines
from machines.Machine import Machine
from machines.StackMachine import StackMachine
from machines.AccuMachine import AccuMachine
from machines.TwoAddressMachine import TwoAddressMachine
from machines.ThreeAddressMachine import ThreeAddressMachine
try:
    from tkinter import *
    from tkinter.ttk import *
except ImportError:
    from Tkinter import *
import gui
from gui import ColorDelegator
from gui import ColoredText
from gui import GUI
import re

def main():
    app = GUI.Application()
    app.mainloop()
if __name__ == '__main__':
    main()
