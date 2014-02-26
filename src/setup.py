#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      said
#
# Created:     23.06.2012
# Copyright:   (c) Awounang Nekdem Franck
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

# A simple setup script to create an executable using Tkinter. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
#
# SimpleTkApp.py is a very simple type of Tkinter application
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

import sys

from cx_Freeze import setup, Executable
"""
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
        name = "PySam",
        version = "0.1",
        description = "Sample cx_Freeze Tkinter script",
        executables = [Executable("GPySam.py", base = base, packages=("gui", "machines")),
                       Executable("PySam.py")])


#!/usr/bin/python
# -*- coding: utf-8 -*-

# source d'inspiration: http://wiki.wxpython.org/cx_freeze
"""
import sys, os
from cx_Freeze import setup, Executable

#############################################################################
# preparation des options
path = sys.path.append(os.path.join("..", "..", "pysam"))
sys.path += ["gui", "machines", "."]

path = "."
includes = ["GUI.py", "ColoredText.py", "GConsole.py", "ColorDelegator.py",
            "machines", "demo.psm"]
excludes = []
packages = ["gui", "machines"]

options = {"path": path,
           "includes": includes,
           "excludes": excludes,
           "packages": packages
           }

#############################################################################
# preparation des cibles
base = None
if sys.platform == "win32":
    base = "Win32GUI"

cible_1 = Executable(
    script = "./GPySam.py",
    base = base,
    compress = True,
    icon = None, **options
    )

cible_2 = Executable(
    script = "PySam.py",
    base = base,
    compress = True,
    icon = None,
    )

#############################################################################
# creation du setup
setup(
    name = "PySam",
    version = "0.1",
    description = "",
    author = "afranck64",
    #options = {"build_exe": options},
    executables = [cible_1,]
    )