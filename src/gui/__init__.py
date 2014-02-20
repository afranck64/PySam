#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      said
#
# Created:     24.06.2012
# Copyright:   (c) said 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import sys
from os import path
sys.argv.append(path.abspath("."))
sys.argv.append(path.abspath(".."))
sys.argv.append(path.abspath("../gui"))
sys.argv.append(path.abspath("gui"))
print (sys.argv)
import GUI
import GConsole
import ColoredText
import ColorDelegator

def main():
    print ("ok")
if __name__ == '__main__':
    main()
