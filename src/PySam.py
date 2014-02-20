#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      said
#
# Created:     23.06.2012
# Copyright:   (c) afranck64 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import machines
import Loader
import sys
import os.path

def main():
    if not len(sys.argv) == 1:
        file = sys.argv[1]
        if os.path.exists(file):
            machine = Loader.getMachine(file=file)
            machine.loop()
        else:
            print ("File not exists :", file)
    else:
        print ("Bad parameter number")


if __name__ == '__main__':
    main()
